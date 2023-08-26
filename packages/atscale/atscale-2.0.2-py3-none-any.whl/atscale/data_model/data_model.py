import copy
import logging
import pandas as pd
from typing import Tuple, List, Dict

from atscale.errors import atscale_errors
from atscale.db.sql_connection import SQLConnection
from atscale.parsers import data_model_parser, project_parser
from atscale.project.project import Project
from atscale.utils import model_utils, project_utils, input_utils, db_utils, request_utils
from atscale.base.enums import PandasTableExistsActionType, PysparkTableExistsActionType, Measure, Level, Hierarchy, FeatureType

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
                     feature_type: FeatureType = FeatureType.ALL) -> pd.DataFrame:
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

        return pd.DataFrame(data=to_df_list,
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

    def get_fact_dataset_names(self) -> List[str]:
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

        allCubeDatasets = self.get_fact_dataset_names()
        matchFoundList = [
            dset for dset in allCubeDatasets if dset == dataset_name]

        return len(matchFoundList) > 0

    def get_column_names(self, dataset_name: str) -> List[str]:
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

        all_column_names = self.get_column_names(dataset_name)
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

    def add_queried_dataset(self, warehouse_id: str, dataset_name: str, query: str,
                            join_features: List[str] = None,
                            join_columns: List[str] = None,
                            roleplay_features: List[str] = None,
                            publish: bool = True,
                            if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL,
                            force_replace: bool = False,
                            delete_children: bool = None,
                            allow_aggregates=True,
                            ):
        """ Creates a new Queried Dataset in this data model which provides results of executing the given query against
        the warehouse of given warehouse_id.

        Args:
            dataset_name(str): The display and query name of the dataset
            query(str): A valid SQL expression with which to directly query the warehouse of the given warehouse_id.
            warehouse_id(str): The warehouse id of the warehouse this qds and its data model are pointing at.
            join_features (list): a list of features in the data model to use for joining.
            join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
                None or the same length and order as join_features. Defaults to None to use identical names to the
                join_features. If multiple columns are needed for a single join they should be in a nested list
            roleplay_features (list, optional): The roleplays to use on the relationships. List must be either
                None or the same length and order as join_features. Use '' to not roleplay that relationship. Defaults to None.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
                if_exists (PandasTableExistsActionType, optional): What to do if a table with table_name already exists. Defaults to PandasTableExistsActionType.FAIL.
            force_replace (bool, optional): When if_exists = REPLACE and this is true, does not prompt. Defaults to False.
            delete_children (bool, optional): Whether dependent features of a dataset should be deleted in the case when
                a dataset already exists and is being replaced. Defaults to None to prompt for input upon this scenario.
            allow_aggregates(bool, optional): Whether aggregates should be built off of this QDS. Defaults to True.
            """
        # check if exists
        if join_features is None:
            join_features = []
        project_dict = self.project._get_dict()
        existing_dset = project_parser.get_dataset_from_datasets_by_name(
            project_datasets=project_parser.get_datasets(
                project_dict=project_dict),
            dataset_name=dataset_name)
        if existing_dset:
            if if_exists == PandasTableExistsActionType.FAIL:
                raise atscale_errors.UserError(
                    f'A dataset already exists with the name {dataset_name}')
            elif if_exists == PandasTableExistsActionType.APPEND:
                raise Exception(
                    f'Appending to a queried dataset is not currently supported')
            else:
                if force_replace == True:
                    delete = True
                else:
                    delete = input_utils.prompt_yes_no(question=f'Dataset {dataset_name} already exists in the project,'
                                                                f'would you like to replace it? This will delete any '
                                                                f'previous usages in any model in this project.')
                if not delete:
                    raise atscale_errors.UserError(f'A dataset already exists with the name {dataset_name} and QDS '
                                                   f'creation has been aborted to protect it.')
                self.project.delete_dataset(dataset_name=dataset_name,
                                            delete_children=delete_children,
                                            publish=False)  # will prompt if it used in any dimensions or measures
                # get fresh dict after deleting dataset
                project_dict = self.project._get_dict()

        columns = self.project.atconn.get_query_columns(warehouse_id=warehouse_id,
                                                        query=query)
        if join_columns is None:
            join_columns = join_features
        elif len(join_features) != len(join_columns):
            raise atscale_errors.UserError(f'join_features and join_columns must be equal lengths. join_features is'
                                           f' length {len(join_features)} while join_columns is length {len(join_columns)}')
        # Verify the join_columns (which may be join_features now) are in the queried columns.
        column_names = {col[0]: True for col in columns}
        missing_columns = [
            join_col for join_col in join_columns if not column_names.get(join_col)]
        if missing_columns:
            raise atscale_errors.UserError(
                f'The given join_columns {missing_columns} are not valid column names in the given query')

        qds_dict = project_utils.create_queried_dataset(name=dataset_name,
                                                        query=query,
                                                        columns=columns,
                                                        warehouse_id=warehouse_id,
                                                        allow_aggregates=allow_aggregates)
        project_dict['datasets'].setdefault('data-set', [])
        project_dict['datasets']['data-set'].append(qds_dict)

        # now add ref to cube
        model_utils.create_dataset_relationship_from_dataset(project_dict=project_dict,
                                                             cube_id=self.cube_id,
                                                             dataset_name=dataset_name,
                                                             join_features=join_features,
                                                             join_columns=join_columns,
                                                             roleplay_features=roleplay_features)

        self.project._update_project(project_json=project_dict,
                                     publish=publish)


    def writeback(self, dbconn: SQLConnection, table_name: str, dataframe: pd.DataFrame, join_features: list, join_columns: list = None, roleplay_features: list = None,
                  publish: bool = True, if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL):
        """Writes the dataframe to a table in the database accessed by dbconn with the given table_name. Joins that table to this
        DataModel by joining on the given join_features or join_columns.

        Args:
            dbconn (SQLConnection): connection to the database; should be the same one the model and project are based on
            table_name (str): the name for the table to be created for the given DataFrame
            dataframe (pd.DataFrame): the pandas DataFrame to write to the database
            join_features (list): a list of features in the data model to use for joining.
            join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
                None or the same length and order as join_features. Defaults to None to use identical names to the
                join_features. If multiple columns are needed for a single join they should be in a nested list
            roleplay_features (list, optional): The roleplays to use on the relationships. List must be either
                None or the same length and order as join_features. Use '' to not roleplay that relationship. Defaults to None.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
            if_exists (PandasTableExistsActionType, optional): What to do if a table with table_name already exists. Defaults to PandasTableExistsActionType.FAIL.
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
        # check_multiple_features(join_features, self.get_all_categorical_features(),
        #                              errmsg='Make sure all items in join_features are categorical features')

        warehouse_id = project_utils.get_project_warehouse(
            self.project._get_dict())

        dbconn.write_df_to_db(table_name=table_name, dataframe=dataframe, if_exists=if_exists)
        database, schema = db_utils.get_database_and_schema(dbconn=dbconn)
        atscale_table_name = db_utils.get_atscale_tablename(atconn=self.project.atconn, warehouse_id=warehouse_id, database=database, schema=schema, table_name=table_name)

        column_dict = db_utils.get_column_dict(atconn=self.project.atconn, dbconn=dbconn,
                                               warehouse_id=warehouse_id, atscale_table_name=atscale_table_name, dataframe_columns=dataframe.columns)

        # If we're replacing a table, then the columns may have changed and the data sets need to be updated.
        if if_exists == PandasTableExistsActionType.REPLACE:
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
                 use_aggs: bool = True, gen_aggs: bool = True, fake_results: bool = False,
                 use_local_cache: bool = True, use_aggregate_cache: bool = True, timeout: int = 10) -> pd.DataFrame:
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
            use_aggs (bool, optional): Whether to allow the query to use aggs. Defaults to True.
            gen_sggs (bool, optional): Whether to allow the query to generate aggs. Defaults to True.
            fake_results (bool, optional): Whether to use fake results. Defaults to False.
            use_local_cache (bool, optional): Whether to allow the query to use the local cache. Defaults to True.
            use_aggregate_cache (bool, optional): Whether to allow the query to use the aggregate cache. Defaults to True.
            timeout (int, optional): The number of minutes to wait for a response before timing out. Defaults to 10.

        Returns:
            DataFrame: A pandas DataFrame containing the query results.
        """

        # avoid a circular import
        from atscale.utils.query_utils import generate_atscale_query
        # set use_aggs and gen_aggs to True because we set them in the json when using the api 
        # and this stops the flags being commented into the query
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

        queryResponse = self.project.atconn._post_query(query, self.project.project_name, use_aggs=use_aggs,
                                                        gen_aggs=gen_aggs, fake_results=fake_results,
                                                        use_local_cache=use_local_cache,
                                                        use_aggregate_cache=use_aggregate_cache,
                                                        timeout=timeout)

        df: pd.DataFrame = request_utils.parse_rest_query_response(
            queryResponse)

        return df

    def get_data_direct(self, dbconn: SQLConnection, feature_list, filter_equals=None, filter_greater=None, filter_less=None,
                        filter_greater_or_equal=None, filter_less_or_equal=None,
                        filter_not_equal=None, filter_in=None, filter_between=None, filter_like=None, filter_rlike=None,
                        filter_null=None,
                        filter_not_null=None, limit=None, comment=None, use_aggs=True, gen_aggs=True) -> pd.DataFrame:
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
            use_aggs (bool, optional): Whether to allow the query to use aggs. Defaults to True.
            gen_aggs (bool, optional): Whether to allow the query to generate aggs. Defaults to True.

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
                                  limit=limit, comment=comment),use_aggs=use_aggs,gen_aggs=gen_aggs))
    
    
    def get_data_jdbc(self, feature_list: List[str], filter_equals: Dict[str, str] = None,
                 filter_greater: Dict[str, str] = None, filter_less: Dict[str, str] = None,
                 filter_greater_or_equal: Dict[str, str] = None, filter_less_or_equal: Dict[str, str] = None,
                 filter_not_equal: Dict[str, str] = None, filter_in: Dict[str, list] = None,
                 filter_between: Dict[str, tuple] = None, filter_like: Dict[str, str] = None,
                 filter_rlike: Dict[str, str] = None, filter_null: List[str] = None,
                 filter_not_null: List[str] = None, limit: int = None, comment: str = None,
                 use_aggs=True, gen_aggs=True) -> pd.DataFrame:
        """Establishes a jdbc connection to Atscale with the supplied information. Then submits query and returns the results in a pandas DataFrame.
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
            use_aggs (bool, optional): Whether to allow the query to use aggs. Defaults to True.
            gen_aggs (bool, optional): Whether to allow the query to generate aggs. Defaults to True.

        Returns:
            DataFrame: A pandas DataFrame containing the query results.
        """
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
                                    comment=comment,
                                    use_aggs=use_aggs,
                                    gen_aggs=gen_aggs)
        conn = self.project.atconn.get_jdbc_connection()
        # can't just use read_sql right now because pandas isn't correctly parsing dates
        #df = pd.read_sql(query, conn)
        curs = conn.cursor()
        curs.execute(query)

        columns = [desc[0] for desc in curs.description]
        types = [desc[1] for desc in curs.description]

        df = pd.DataFrame(curs.fetchall(), columns=columns) 
        for (column, type) in list(zip(columns,types)):
            type_lower = type.values[0].lower()
            if 'date' in type_lower or 'time' in type_lower:
                df[column] = pd.to_datetime(df[column], errors='coerce', infer_datetime_format=True)
        return df


    def get_data_spark(self, feature_list: List[str], sparkSession, jdbc_format: str, jdbc_options: Dict[str,str],
                 filter_equals: Dict[str, str] = None, filter_greater: Dict[str, str] = None, 
                 filter_less: Dict[str, str] = None, filter_greater_or_equal: Dict[str, str] = None, 
                 filter_less_or_equal: Dict[str, str] = None, filter_not_equal: Dict[str, str] = None, 
                 filter_in: Dict[str, list] = None, filter_between: Dict[str, tuple] = None, 
                 filter_like: Dict[str, str] = None, filter_rlike: Dict[str, str] = None, 
                 filter_null: List[str] = None, filter_not_null: List[str] = None, limit: int = None, 
                 comment: str = None, use_aggs=True, gen_aggs=True):
        """Uses the provided information to establish a jdbc connection to the underlying dwh. Generates a query and uses
            the provided sparkSession to execute. Returns the results in a spark DataFrame.
        Args:
            feature_list (List[str]): The list of features to query.
            sparkSession (pyspark.sql.SparkSession): The pyspark SparkSession to execute the query with
            jdbc_format (str): the driver class name. For example: 'jdbc', 'net.snowflake.spark.snowflake', 'com.databricks.spark.redshift' 
            jdbc_options (Dict[str,str]): Case-insensitive to specify connection options for jdbc 
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
            use_aggs (bool, optional): Whether to allow the query to use aggs. Defaults to True.
            gen_aggs (bool, optional): Whether to allow the query to generate aggs. Defaults to True.
        Returns:
            pyspark.sql.DataFrame: A pyspark DataFrame containing the query results.
        """
        # avoid a circular import
        from atscale.utils.query_utils import generate_atscale_query, generate_db_query
        
        try:
            from pyspark.sql import SparkSession 
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError('jdbc', str(e))

        query = generate_db_query(self, generate_atscale_query(data_model=self, feature_list=feature_list,
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
                                                comment=comment), use_aggs=use_aggs, gen_aggs=gen_aggs)

        df = sparkSession.read.format(jdbc_format).options(**jdbc_options) \
                        .option("query", query).load()

        column_index = range(len(df.columns))
        column_names = df.columns
        
        for column in column_index:
            df = df.withColumnRenamed(column_names[column], feature_list[column])

        return df

    def writeback_spark(self, dbconn: SQLConnection, pyspark_dataframe, jdbc_format: str, jdbc_options: Dict[str,str],
                  join_features: list, table_name: str = None, join_columns: list = None, roleplay_features: list = None,
                  publish: bool = True, if_exists: PysparkTableExistsActionType = PysparkTableExistsActionType.ERROR):
        """Writes the pyspark dataframe to a table in the database accessed via jdbc with the given table_name. Joins that table to this
        DataModel by joining on the given join_features or join_columns.

        Args:
            dbconn (SQLConnection): connection to the database; should be the same one the model and project are based on
            pyspark_dataframe (pyspark.sql.DataFrame): The pyspark dataframe to write
            jdbc_format (str): the driver class name. For example: 'jdbc', 'net.snowflake.spark.snowflake', 'com.databricks.spark.redshift' 
            jdbc_options (Dict[str,str]): Case-insensitive to specify connection options for jdbc. The query option is dynamically generated by
                atscale, as a result including a table or query parameter can cause issues. 
            dataframe (DataFrame): the DataFrame to write to the database
            join_features (list): a list of features in the data model to use for joining.
            table_name (str, optional): The name for the table to be created for the given PySpark DataFrame. Can be none if name specified in options
            join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
                None or the same length and order as join_features. Defaults to None to use identical names to the
                join_features. If multiple columns are needed for a single join they should be in a nested list
            roleplay_features (list, optional): The roleplays to use on the relationships. List must be either
                None or the same length and order as join_features. Use '' to not roleplay that relationship. Defaults to None.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
            if_exists (PysparkTableExistsActionType, optional): What to do if a table with table_name already exists. Defaults to PysparkTableExistsActionType.ERROR.
        """
        #import the needed spark packages
        try:
            from pyspark.sql import DataFrame
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError('jdbc', str(e))

        if join_columns is None:
            join_columns = join_features

        if len(join_features) != len(join_columns):
            raise atscale_errors.UserError(f'join_features and join_columns must be equal lengths. join_features is'
                                           f' length {len(join_features)} while join_columns is length {len(join_columns)}')

        # Verify the join_columns (which may be join_features now) are in the dataframe columns.
        # There was a method for this called check_multiple_features but this is a one-liner.
        # The check was commented out, but seems like a good one, so throwing it back in.
        if not all(item in pyspark_dataframe.columns for item in join_columns):
            raise atscale_errors.UserError(
                'Make sure all items in join_columns are in the dataframe')


        ### We may need to pass on this check. We would need to hardcode the various jdbc formats/options per sqlconnection type and then use 
        ### the hardcoded values to get the warehouse, database, schema from the passed options. That is assuming there aren't
        ### other ways to set up the jdbc connection or use other jdbc formats. Seems very fragile to me.

        # # verify our sql_connection is pointed at a connection that the model points at, and we'll use
        # # that info later for join tables
        # project_datasets = self._get_referenced_project_datasets()
        # connex = self.project.atconn._get_connection_groups()
        # project_datasets, connections = dbconn._verify_connection(
        #     project_datasets, connex)
        # if connections is None or len(connections) < 1:
        #     msg = 'The SQLConnection connects to a database or schema that is not referenced by the given data_model.'
        #     logger.exception(msg)
        #     raise atscale_errors.UserError(msg)


        warehouse_id = project_utils.get_project_warehouse(
            self.project._get_dict())

        dbconn.write_pysparkdf_to_db(pyspark_dataframe= pyspark_dataframe, jdbc_format= jdbc_format, jdbc_options= jdbc_options, 
                                    table_name=table_name, if_exists=if_exists)
        database, schema = db_utils.get_database_and_schema(dbconn=dbconn)
        atscale_table_name = db_utils.get_atscale_tablename(atconn=self.project.atconn, warehouse_id=warehouse_id, database=database, schema=schema, table_name=table_name)

        column_dict = db_utils.get_column_dict(atconn=self.project.atconn, dbconn=dbconn,
                                               warehouse_id=warehouse_id, atscale_table_name=atscale_table_name, dataframe_columns=pyspark_dataframe.columns)

        # If we're replacing a table, then the columns may have changed and the data sets need to be updated.
        if if_exists == PysparkTableExistsActionType.OVERWRITE:
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
