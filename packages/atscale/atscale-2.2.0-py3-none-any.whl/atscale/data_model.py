import copy
import logging
from typing import Tuple, List, Dict

from pandas import DataFrame

from atscale import atscale_errors
from atscale.db.sql_connection import SQLConnection
from atscale.parsers import data_model_parser, response_parser
from atscale.parsers import project_parser
from atscale.project import Project
from atscale.utils import db_utils
from atscale.utils import model_utils
from atscale.utils import project_utils
from atscale.utils.enums import Measure, Level, Hierarchy, FeatureType
from atscale.utils.enums import TableExistsActionType
from atscale.utils.project_utils import get_project_warehouse

logger = logging.getLogger(__name__)


class DataModel:
    """Creates an object corresponding to an AtScale Data Model. Takes an existing model id and 
        AtScale Project object to construct an object that deals with functionality related to model level
        datasets and columns, as well as reading data and writing back predictions.
    """

    def __init__(self, data_model_id: str, project: Project):
        """A Data Model is an abstraction that represents a perspective or cube within AtScale.

        Args:
            data_model_id (str): the unique identifier of the model in question
            project (Project): the AtScale Project object the model is a part of
        """

        if data_model_id is None:
            raise ValueError("data_model_id must be provided.")

        self.__id = data_model_id

        if project is None:
            raise ValueError("Project must be provided.")

        # I use the public setter so it's logic is executed instead of setting local variable direclty.
        # I piggy back on this call to set the data_model_name and cube_ref. This is just to not have duplicate
        # code here and also in the project settr for getting json, parsing, etc. It has to happen in the
        # settr anyway, and having an extra call to set the name and cube_ref if it already made the REST
        # call and parsed out the data model should be pretty trivial.
        self.project = project

    @property
    def id(self) -> str:
        """Getter for the id instance variable

        Returns:
            str: The id of this model
        """
        return self.__id

    @id.setter
    def id(self, value):
        """Setter for the id instance variable. This variable is final, please construct a new DataModel.

        Args:
            value: setter cannot be used.

        Raises:
            Exception: Raises a value if the setter is attempted.
        """
        raise Exception(
            'Value of data_model_id is final; it cannot be reset. Please construct a new DataModel instead.')

    @property
    def cube_id(self) -> str:
        """Getter for the id of the source cube. If the DataModel is a perspective this will 
            return the reference id for the source cube.

        Returns:
            str: The id of the source cube.
        """
        return self.__cube_ref if self.is_perspective() else self.__id

    @property
    def name(self) -> str:
        """Getter for the name instance variable. The name of the cube.

        Returns:
            str: The textual identifier for the cube.
        """
        return self.__name

    @name.setter
    def name(self, value):
        """Setter for the name instance variable. This variable is final, please construct a new DataModel.

        Args:
            value: setter cannot be used.

        Raises:
            Exception: Raises a value if the setter is attempted.
        """
        raise Exception(
            'Value of data model name is final; it cannot be reset')

    @property
    def project(self) -> Project:
        """Getter for the Project instance variable.

        Returns:
            Project: The Project object this model belongs to.
        """
        return self.__project

    @project.setter
    def project(self, value: Project):
        """Setter for Project instance variable.

        Args:
            value (Project): The new project to associate the model with.

        Raises:
            ValueError: If the new Project is not associated with the DataModel.
        """
        if value is None:
            raise ValueError("The provided value is None.")
        if not isinstance(value, Project):
            raise ValueError("The provided value is not a Project.")
        project_dict = value._get_dict()
        data_model_dict = project_parser.get_data_model(
            project_dict, self.__id)
        if not data_model_dict:
            raise ValueError(
                "The provided Project is not associated with this DataModel.")
        self.__project = value
        # If data_model_dict is a cube, then it will have no cube-ref key, and __cube_ref will be set to None, which is valid.
        # If data_model_dict is a perspective, then it will have the key,  and cube_ref will be set.
        self.__cube_ref = data_model_dict.get('cube-ref')
        self.__name = data_model_dict.get('name')

    def get_features(self, feature_list: List[str] = None, folder_list: List[str] = None,
                     feature_type: FeatureType = FeatureType.ALL) -> DataFrame:
        """Gets the data type, description, expression, folder, and feature type for each feature in the DataModel.

        Args:
            feature_list (List[str], optional): A list of features to return. Defaults to None to return all.
            folder_list (List[str], optional): A list of folders to filter by. Defaults to None to ignore folder.
            feature_type (FeatureType, optional): The type of features to filter by. Options
                include FeatureType.ALL, FeatureType.CATEGORICAL, or FeatureType.NUMERIC. Defaults to ALL.

        Returns:
            pandas.DataFrame: A DataFrame with a row for each feature, and the following columns:
                'name', 'data type'(value is a level-type, 'Aggregate', or 'Calculated'), 'description', 'expression',
                'folder', and 'feature type'(Numeric or Categorical).
        """
        from atscale.utils.dmv_utils import get_dmv_data
        level_filter_by = {}
        measure_filter_by = {}
        hier_filter_by = {}
        if feature_list:
            feature_list = [feature_list] if isinstance(
                feature_list, str) else feature_list
            level_filter_by[Level.name] = feature_list
            measure_filter_by[Measure.name] = feature_list
        if folder_list:
            folder_list = [folder_list] if isinstance(
                folder_list, str) else folder_list
            hier_filter_by[Hierarchy.folder] = folder_list
            measure_filter_by[Measure.folder] = folder_list

        to_df_level_list = []
        to_df_measure_list = []

        if feature_type is FeatureType.ALL or feature_type is FeatureType.CATEGORICAL:
            hier_dict = get_dmv_data(model=self,
                                     fields=[Hierarchy.folder],
                                     filter_by=hier_filter_by)
            level_filter_by[Level.hierarchy] = list(hier_dict.keys())

            dimension_dict = get_dmv_data(
                model=self,
                fields=[Level.type, Level.description, Level.hierarchy],
                filter_by=level_filter_by
            )

            to_df_level_list = [[
                dimension,
                dimension_dict[dimension][Level.type.name],
                dimension_dict[dimension][Level.description.name],
                '',
                hier_dict[dimension_dict[dimension]
                          [Level.hierarchy.name]][Hierarchy.folder.name],
                'Categorical'
            ] for dimension in dimension_dict]

        if feature_type is FeatureType.ALL or feature_type is FeatureType.NUMERIC:
            measure_dict = get_dmv_data(
                model=self,
                fields=[Measure.type, Measure.description,
                        Measure.expression, Measure.folder],
                filter_by=measure_filter_by
            )

            to_df_measure_list = [[
                measure,
                measure_dict[measure][Measure.type.name],
                measure_dict[measure][Measure.description.name],
                measure_dict[measure][Measure.expression.name],
                measure_dict[measure][Measure.folder.name],
                'Numeric'
            ] for measure in measure_dict]

        to_df_list = to_df_level_list + to_df_measure_list

        return DataFrame(data=to_df_list,
                         columns=['name', 'data type', 'description', 'expression', 'folder', 'feature type'])

    def is_perspective(self) -> bool:
        """Checks if this DataModel is a perspective

        Returns:
            bool: true if this is a perspective
        """
        if self.__cube_ref:
            return True
        else:
            return False

    def _get_model_dict(self) -> Tuple[dict, dict]:
        """Returns one or two dictionaries associated with this data_model

        Returns:
            Tuple[dict, dict]: returns the cube and perspective respectively, where perspective may be None
        """
        cube_dict = None
        perspective_dict = None
        project_dict = self.__project._get_dict()
        if self.is_perspective():
            perspective_dict = project_parser.get_data_model(
                project_dict, self.__id)
            cube_dict = project_parser.get_data_model(
                project_dict, self.__cube_ref)
        else:
            cube_dict = project_parser.get_data_model(project_dict, self.__id)
        return cube_dict, perspective_dict

    def _get_referenced_project_datasets(self) -> List[dict]:
        """Returns a list of all project datasets referenced by this model.

        Returns:
            list[dict]: list of all project datasets referenced by this model
        """
        return data_model_parser.get_project_datasets_referenced_by_cube(
            self.__project._get_dict(), self._get_model_dict()[0])

    def list_fact_datasets(self) -> List[str]:
        """Gets the name of all fact datasets currently utilized by the DataModel and returns as a list.

        Returns:
            List[str]: list of fact dataset names
        """
        all_datasets = data_model_parser.get_project_datasets_referenced_by_cube(
            self.__project._get_dict(), self._get_model_dict()[0])
        if len(all_datasets) > 0:
            return [dataset.get('name') for dataset in all_datasets]
        return all_datasets

    def dataset_exists(self, dataset_name: str) -> bool:
        """Returns whether a given dataset_name exists in the data model, case-sensitive.

        Args:
            dataset_name (str): the name of the dataset to try and find

        Returns:
            bool: true if name found, else false.
        """

        allCubeDatasets = self.list_fact_datasets()
        matchFoundList = [
            dset for dset in allCubeDatasets if dset == dataset_name]

        return len(matchFoundList) > 0

    def list_columns(self, dataset_name: str) -> List[str]:
        """Gets a list of all currently visible columns in a given dataset, case-sensitive.

        Args:
            dataset_name (str): the name of the dataset to get columns from, case-sensitive.

        Returns:
            List[str]: the column names in the given dataset
        """

        if not self.dataset_exists(dataset_name):
            raise atscale_errors.UserError(
                f"Dataset: '{dataset_name}' not found.")

        dataset_of_int = project_parser.get_dataset_from_datasets_by_name(project_parser.get_datasets(
            self.__project._get_dict()), dataset_name)

        physical_list = dataset_of_int.get('physical')
        if physical_list is None:
            return []

        column_list = physical_list.get('columns', [])

        for map_col in physical_list.get('map-column', []):
            column_list += map_col.get('columns', {}).get('columns', [])

        return [columnVal.get('name') for columnVal in column_list]

    def column_exists(self, dataset_name: str, column_name: str) -> bool:
        """Checks if the given column name exists in the dataset.

        Args:
            dataset_name (str): the name of the dataset we pull the columns from, case-sensitive.
            column_name (str): the name of the column to check, case-sensitive

        Returns:
            bool: true if name found, else false.
        """

        all_column_names = self.list_columns(dataset_name)
        match_found_list = [
            col_name for col_name in all_column_names if col_name == column_name]

        return len(match_found_list) > 0

    def delete_measures(self, measure_list: List[str], publish: bool = True, delete_children: bool = None):
        """Deletes a list of measures from the DataModel. If a measure is referenced in any calculated measures,
         and delete_children is not set, then the user will be prompted with a list of children measures and given the
         choice to delete them or abort.

        Args:
            measure_list (List[str]): the query names of the measures to be deleted
            publish (bool, optional): Defaults to True, whether the updated project should be published
            delete_children (bool, optional): Defaults to None, if set to True or False no prompt will be given in the case of
                any other measures being derived from the given measure_name. Instead, these measures will also be deleted when
                delete_children is True, alternatively, if False, the method will be aborted with no changes to the data model

        Raises:
            DependentMeasureException: if child measures are encountered and the method is aborted
            atscale_errors.UserError: if a measure_name is not found in the data model"""

        json_dict = copy.deepcopy(self.project._get_dict())
        from atscale.utils import feature_utils
        feature_utils._delete_measures_local(data_model=self,
                                             measure_list=measure_list,
                                             json_dict=json_dict,
                                             delete_children=delete_children)
        self.project._update_project(project_json=json_dict,
                                     publish=publish)

    def add_dataset(self, warehouse_id, database, schema, table_name, publish=True):
        project_dict = self.project._get_dict()
        cube_dict = project_parser.get_cube(project_dict, self.cube_id)
        # get the columns, as atscale sees them (i.e. with the atscale types necessary for dataset specification)
        columns = self.project.atconn.get_table_columns(warehouse_id=warehouse_id,
                                                        table_name=table_name,
                                                        database=database,
                                                        schema=schema)
        # create the project dataset which the cube will then reference
        dataset, dataset_id = project_utils.create_dataset(warehouse_id=warehouse_id,
                                                           database=database,
                                                           schema=schema,
                                                           table_name=table_name,
                                                           table_columns=columns)
        # add the newly minted dataset to the project_dict
        #setdefault only sets the value if it is currently None
        project_dict['datasets'].setdefault('data-set', [])
        project_dict['datasets']['data-set'].append(dataset)
        # create and add the dataset reference to the cube
        data_set_ref = model_utils.create_dataset_ref(dataset_id)
        cube_dict.setdefault('data-sets', {})
        cube_dict['data-sets'].setdefault('data-set-ref', [])
        cube_dict['data-sets']['data-set-ref'].append(data_set_ref)
        self.project._update_project(project_json=project_dict, publish=publish)

    def writeback(self, dbconn: SQLConnection, table_name: str, dataframe: DataFrame, join_features: list, join_columns: list = None, roleplay_features: list = None,
                  publish: bool = True, if_exists: TableExistsActionType = TableExistsActionType.FAIL):
        """Writes the dataframe to a table in the database accessed by dbconn with the given table_name. Joins that table to this
        DataModel by joining on the given join_features or join_columns.

        Args:
            dbconn (SQLConnection): connection to the database; should be the same one the model and project are based on
            table_name (str): the name for the table to be created for the given DataFrame
            dataframe (DataFrame): the DataFrame to write to the database
            join_features (list): a list of features in the data model to use for joining.
            join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
                None or the same length and order as join_features. Defaults to None to use identical names to the
                join_features. If multiple columns are needed for a single join they should be in a nested list
            roleplay_features (list, optional): The roleplays to use on the relationships. List must be either
                None or the same length and order as join_features. Use '' to not roleplay that relationship. Defaults to None.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
            if_exists (TableExistsActionType, optional): What to do if a table with table_name already exists. Defaults to TableExistsActionType.FAIL.
        """
        if join_columns is None:
            join_columns = join_features

        if len(join_features) != len(join_columns):
            raise atscale_errors.UserError(f'join_features and join_columns must be equal lengths. join_features is'
                                           f' length {len(join_features)} while join_columns is length {len(join_columns)}')

        # Verify the join_columns (which may be join_features now) are in the dataframe columns.
        # There was a method for this called check_multiple_features but this is a one-liner.
        # The check was commented out, but seems like a good one, so throwing it back in.
        if not all(item in dataframe.columns for item in join_columns):
            raise atscale_errors.UserError(
                'Make sure all items in join_columns are in the dataframe')

        # verify our sql_connection is pointed at a connection that the model points at, and we'll use
        # that info later for join tables
        project_datasets = self._get_referenced_project_datasets()
        connex = self.project.atconn._get_connection_groups()
        project_datasets, connections = dbconn._verify_connection(
            project_datasets, connex)
        if connections is None or len(connections) < 1:
            msg = 'The SQLConnection connects to a database or schema that is not referenced by the given data_model.'
            logger.exception(msg)
            raise atscale_errors.UserError(msg)

        # this was commented out in atscale_comments - leaving commented for now until we get more info
        # check_multiple_features(join_features, self.list_all_categorical_features(),
        #                              errmsg='Make sure all items in join_features are categorical features')

        warehouse_id = get_project_warehouse(self.project._get_dict())
        atscale_table_name, column_dict = db_utils.write_dataframe_to_db(atconn=self.project.atconn, dbconn=dbconn, warehouse_id=warehouse_id,
                                                                         table_name=table_name,  dataframe=dataframe, if_exists=if_exists)

        # If we're replacing a table, then the columns may have changed and the data sets need to be updated.
        if if_exists == TableExistsActionType.REPLACE:
            self.project._update_project_tables([atscale_table_name], False)

        # TODO Question
        # I would imagine that if we are adding a new table entirely, we also need to update_project_tables, but not sure?
        # It wasn't in the original code, so leaving it out for now.
        atscale_join_columns = []
        for col in join_columns:
            if type(col) is list:
                nested_list = []
                for nested_col in col:
                    nested_list.append(column_dict[nested_col])
                atscale_join_columns.append(nested_list)
            else:
                atscale_join_columns.append(column_dict[col])
        # TODO: connect with John Lynch and potentially rethink this code. Some SQLConnection
        # implementations do not have a database or schema variable to even call and see if it's None.
        # So for now I'll just determine if they even have that attribute with introspection in addition
        # to checking it's value, but seems like there may be a smoother approach. Also not sure what
        # will happen in join_table below which currently requires a schema value
        database = None
        schema = None
        if hasattr(dbconn, 'database'):
            database = dbconn.database
        if hasattr(dbconn, 'schema'):
            schema = dbconn.schema

        # join_table now mutates the project_json and returns, then we're responsible for posting
        project_dict = model_utils.create_dataset_relationship(atconn=self.project.atconn, project_dict=self.project._get_dict(), cube_id=self.cube_id,
                                                               database=database, schema=schema, table_name=atscale_table_name, join_features=join_features, join_columns=atscale_join_columns, roleplay_features=roleplay_features)

        self.project._update_project(
            project_json=project_dict, publish=publish)

    def join_table(self, table_name: str, join_features: List[str], database: str = None, schema: str = None, join_columns: List[str] = None, roleplay_features: List[str] = None, publish: bool = True):
        """Join a table in the data warehouse to the data model

        Args:
            table_name (str): The table to join
            join_features (List[str]): The features in the data model to join on
            database (str, optional): The database the table belongs to if relevant for the data warehouse. Defaults to None.
            schema (str, optional): The schema the table belongs to if relevant for the data warehouse. Defaults to None.
            join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
                None or the same length and order as join_features. Defaults to None to use identical names to the
                join_features. If multiple columns are needed for a single join they should be in a nested list
            roleplay_features (List[str], optional): The roleplays to use on the relationships. List must be either
                None or the same length and order as join_features. Use '' to not roleplay that relationship. Defaults to None.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
        """
        project_dict = model_utils.create_dataset_relationship(atconn=self.project.atconn, project_dict=self.project._get_dict(), cube_id=self.cube_id,
                                                               database=database, schema=schema, table_name=table_name, join_features=join_features, join_columns=join_columns, roleplay_features=roleplay_features)

        self.project._update_project(
            project_json=project_dict, publish=publish)

    def get_data(self, feature_list: List[str], filter_equals: Dict[str, str] = None,
                 filter_greater: Dict[str, str] = None, filter_less: Dict[str, str] = None,
                 filter_greater_or_equal: Dict[str, str] = None, filter_less_or_equal: Dict[str, str] = None,
                 filter_not_equal: Dict[str, str] = None, filter_in: Dict[str, list] = None,
                 filter_between: Dict[str, tuple] = None, filter_like: Dict[str, str] = None,
                 filter_rlike: Dict[str, str] = None, filter_null: List[str] = None,
                 filter_not_null: List[str] = None, limit: int = None, comment: str = None,
                 useAggs: bool = True, genAggs: bool = False, fakeResults: bool = False,
                 useLocalCache: bool = True, useAggregateCache: bool = True, timeout: int = 2) -> DataFrame:
        """Submits a query using the supplied information and returns the results in a pandas DataFrame.

        Args:
            feature_list (List[str]): The list of features to query.
            filter_equals (Dict[str, str], optional): Filters results based on the feature equaling the value. Defaults to None.
            filter_greater (Dict[str, str], optional): Filters results based on the feature being greater than the value. Defaults to None.
            filter_less (Dict[str, str], optional): Filters results based on the feature being less than the value. Defaults to None.
            filter_greater_or_equal (Dict[str, str], optional): Filters results based on the feature being greater or equaling the value. Defaults to None.
            filter_less_or_equal (Dict[str, str], optional): Filters results based on the feature being less or equaling the value. Defaults to None.
            filter_not_equal (Dict[str, str], optional): Filters results based on the feature not equaling the value. Defaults to None.
            filter_in (Dict[str, list], optional): Filters results based on the feature being contained in the values. Defaults to None.
            filter_between (Dict[str, tuple], optional): Filters results based on the feature being between the values. Defaults to None.
            filter_like (Dict[str, str], optional): Filters results based on the feature being like the clause. Defaults to None.
            filter_rlike (Dict[str, str], optional): Filters results based on the feature being matched by the regular expression. Defaults to None.
            filter_null (List[str], optional): Filters results to show null values of the specified features. Defaults to None.
            filter_not_null (List[str], optional): Filters results to exclude null values of the specified features. Defaults to None.
            limit (int, optional): Limit the number of results. Defaults to None for no limit.
            comment (str, optional): A comment string to build into the query. Defaults to None for no comment.
            useAggs (bool, optional): Whether to allow the query to use aggs. Defaults to True.
            genAggs (bool, optional): Whether to allow the query to generate aggs. Defaults to False.
            fakeResults (bool, optional): Whether to use fake results. Defaults to False.
            useLocalCache (bool, optional): Whether to allow the query to use the local cache. Defaults to True.
            useAggregateCache (bool, optional): Whether to allow the query to use the aggregate cache. Defaults to True.
            timeout (int, optional): The number of minutes to wait for a response before timing out. Defaults to 2.

        Returns:
            DataFrame: A pandas DataFrame containing the query results.
        """

        # avoid a circular import
        from atscale.utils.query_utils import generate_atscale_query
        query = generate_atscale_query(data_model=self, feature_list=feature_list,
                                       filter_equals=filter_equals,
                                       filter_greater=filter_greater,
                                       filter_less=filter_less,
                                       filter_greater_or_equal=filter_greater_or_equal,
                                       filter_less_or_equal=filter_less_or_equal,
                                       filter_not_equal=filter_not_equal,
                                       filter_in=filter_in,
                                       filter_between=filter_between,
                                       filter_like=filter_like,
                                       filter_rlike=filter_rlike,
                                       filter_null=filter_null,
                                       filter_not_null=filter_not_null,
                                       limit=limit,
                                       comment=comment)

        queryResponse = self.project.atconn._post_query(query, self.project.project_name, useAggs=useAggs,
                                                        genAggs=genAggs, fakeResults=fakeResults,
                                                        useLocalCache=useLocalCache,
                                                        useAggregateCache=useAggregateCache,
                                                        timeout=timeout)

        df: DataFrame = response_parser.parse_rest_query_response(
            queryResponse)

        return df

    def get_data_direct(self, dbconn: SQLConnection, feature_list, filter_equals=None, filter_greater=None, filter_less=None,
                        filter_greater_or_equal=None, filter_less_or_equal=None,
                        filter_not_equal=None, filter_in=None, filter_between=None, filter_like=None, filter_rlike=None,
                        filter_null=None,
                        filter_not_null=None, limit=None, comment=None) -> DataFrame:
        """Generates an AtScale query to get the given features, translates it to a database query, and
        submits it directly to the database using the SQLConnection. The results are returned as a Pandas DataFrame
        Args:
            dbconn (SQLConnection): The connection to use to submit the query to the database.
            feature_list (List[str]): The list of features to query.
            filter_equals (Dict[str, str], optional): A dictionary of features to filter for equality to the value. Defaults to None.
            filter_greater (Dict[str, str], optional): A dictionary of features to filter greater than the value. Defaults to None.
            filter_less (Dict[str, str], optional): A dictionary of features to filter less than the value. Defaults to None.
            filter_greater_or_equal (Dict[str, str], optional): A dictionary of features to filter greater than or equal to the value. Defaults to None.
            filter_less_or_equal (Dict[str, str], optional): A dictionary of features to filter less than or equal to the value. Defaults to None.
            filter_not_equal (Dict[str, str], optional): A dictionary of features to filter not equal to the value. Defaults to None.
            filter_in (Dict[str, list], optional): A dictionary of features to filter in a list. Defaults to None.
            filter_between (Dict[str, tuple], optional): A dictionary of features to filter between the tuple values. Defaults to None.
            filter_like (Dict[str, str], optional): A dictionary of features to filter like the value. Defaults to None.
            filter_rlike (Dict[str, str], optional): A dictionary of features to filter rlike the value. Defaults to None.
            filter_null (List[str], optional): A list of features to filter for null. Defaults to None.
            filter_not_null (List[str], optional): A list of features to filter for not null. Defaults to None.
            limit (int, optional): A limit to put on the query. Defaults to None.
            comment (str, optional): A comment to put in the query. Defaults to None.

        Returns:
            DataFrame: The results of the query as a DataFrame
        """
        from atscale.utils.query_utils import generate_db_query, generate_atscale_query  # avoid circular import
        return dbconn.submit_query(
            generate_db_query(data_model=self,
                              atscale_query=generate_atscale_query(
                                  data_model=self,
                                  feature_list=feature_list, filter_equals=filter_equals, filter_greater=filter_greater,
                                  filter_less=filter_less, filter_greater_or_equal=filter_greater_or_equal,
                                  filter_less_or_equal=filter_less_or_equal, filter_not_equal=filter_not_equal,
                                  filter_in=filter_in, filter_between=filter_between, filter_like=filter_like,
                                  filter_rlike=filter_rlike, filter_null=filter_null, filter_not_null=filter_not_null,
                                  limit=limit, comment=comment)))
