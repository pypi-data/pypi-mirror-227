import copy
import logging
import pandas as pd
from typing import List, Dict, Union

from atscale.errors import atscale_errors
from atscale.db.sql_connection import SQLConnection
from atscale.parsers import data_model_parser, project_parser, dictionary_parser
from atscale.project.project import Project
from atscale.utils import model_utils, metadata_utils,  project_utils, input_utils, db_utils, request_utils, dimension_utils, feature_utils, query_utils
from atscale.base.enums import PandasTableExistsActionType, PysparkTableExistsActionType, Measure, Level, Hierarchy, FeatureType, MappedColumnDataTypes
from atscale.base.enums import MappedColumnKeyTerminator, MappedColumnFieldTerminator, FeatureFormattingType, Aggs, MDXAggs
from atscale.utils.dmv_utils import get_dmv_data
from atscale.data_model import data_model_helpers

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
        """Getter for the name instance variable. The name of the data model.

        Returns:
            str: The textual identifier for the data model.
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
                     feature_type: FeatureType = FeatureType.ALL, use_published: bool = True) -> dict:
        """Gets the feature names and metadata for each feature in the published DataModel.

        Args:
            feature_list (List[str], optional): A list of features to return. Defaults to None to return all.
            folder_list (List[str], optional): A list of folders to filter by. Defaults to None to ignore folder.
            feature_type (FeatureType, optional): The type of features to filter by. Options
                include FeatureType.ALL, FeatureType.CATEGORICAL, or FeatureType.NUMERIC. Defaults to ALL.
            use_published (bool, optional): whether to get the features of the published or unpublished data model.
                Defaults to True to use the published version.

        Returns:
            dict: A dictionary of dictionaries where the feature names are the keys in the outer dictionary 
                  while the inner keys are the following: 'data_type'(value is a level-type, 'Aggregate', or 'Calculated'), 
                  'description', 'expression', caption, 'folder', and 'feature_type'(value is Numeric or Categorical).
        """

        if use_published:
            ret_dict =  data_model_helpers._get_published_features(self, feature_list= feature_list, folder_list= folder_list,
                                                                  feature_type= feature_type)
        else:
            project_dict = self.project._get_dict()
            ret_dict =  data_model_helpers._get_unpublished_features(project_dict, data_model_name = self.name, feature_list = feature_list,
                                                                     folder_list = folder_list, feature_type = feature_type)
        return ret_dict

    def is_perspective(self) -> bool:
        """Checks if this DataModel is a perspective

        Returns:
            bool: true if this is a perspective
        """
        if self.__cube_ref:
            return True
        else:
            return False

    def _get_referenced_project_datasets(self) -> List[dict]:
        """Returns a list of all project datasets referenced by this model.

        Returns:
            list[dict]: list of all project datasets referenced by this model
        """
        project_dict = self.__project._get_dict()
        return data_model_parser.get_project_datasets_referenced_by_cube(
            project_dict, model_utils._get_model_dict(data_model=self,
                                     project_dict= project_dict)[0])

    def get_fact_dataset_names(self) -> List[str]:
        """Gets the name of all fact datasets currently utilized by the DataModel and returns as a list.

        Returns:
            List[str]: list of fact dataset names
        """
        project_dict = self.__project._get_dict()
        return model_utils._get_fact_dataset_names(self, project_dict)

    def get_dimension_dataset_names(self) -> List[str]:
        """Gets the name of all dimension datasets currently utilized by the DataModel and returns as a list.

        Returns:
            List[str]: list of dimension dataset names
        """
        project_dict = self.__project._get_dict()
        return model_utils._get_dimension_dataset_names(self, project_dict)

    def get_dataset_names(self) -> List[str]:
        """Gets the name of all datasets currently utilized by the DataModel and returns as a list.

        Returns:
            List[str]: list of dataset names
        """
        project_dict = self.__project._get_dict()
        return list(set(model_utils._get_fact_dataset_names(self, project_dict) + model_utils._get_dimension_dataset_names(self, project_dict)))

    def dataset_exists(self, dataset_name: str) -> bool:
        """Returns whether a given dataset_name exists in the data model, case-sensitive.

        Args:
            dataset_name (str): the name of the dataset to try and find

        Returns:
            bool: true if name found, else false.
        """
        return dataset_name in self.get_dataset_names()

    def get_column_names(self, dataset_name: str) -> List[str]:
        """Gets a list of all currently visible columns in a given dataset, case-sensitive.

        Args:
            dataset_name (str): the name of the dataset to get columns from, case-sensitive.

        Returns:
            List[str]: the column names in the given dataset
        """
        project_dict = self.__project._get_dict()

        if not self.dataset_exists(dataset_name):
            raise atscale_errors.UserError(
                f"Dataset: '{dataset_name}' not found.")

        return model_utils._get_column_names(project_dict, dataset_name=dataset_name)

    def column_exists(self, dataset_name: str, column_name: str) -> bool:
        """Checks if the given column name exists in the dataset.

        Args:
            dataset_name (str): the name of the dataset we pull the columns from, case-sensitive.
            column_name (str): the name of the column to check, case-sensitive

        Returns:
            bool: true if name found, else false.
        """
        project_dict = self.__project._get_dict()

        if not self.dataset_exists(dataset_name):
            raise atscale_errors.UserError(
                f"Dataset: '{dataset_name}' not found.")

        return model_utils._column_exists(project_dict, dataset_name=dataset_name,
                                            column_name= column_name)

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

        model_utils._perspective_check(self, 'Delete operations are not supported for perspectives.')

        json_dict = copy.deepcopy(self.project._get_dict())
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
            warehouse_id(str): The warehouse id of the warehouse this qds and its data model are pointing at.
            dataset_name(str): The display and query name of the dataset
            query(str): A valid SQL expression with which to directly query the warehouse of the given warehouse_id.
            join_features (list, optional): a list of features in the data model to use for joining. If None it will not
                join the qds to anything. Defaults to None.
            join_columns (list, optional): The columns in the dataset to join to the join_features. List must be either
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
        model_utils._perspective_check(self)

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

        if join_features is not None:
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
        project_utils.add_dataset(project_dict=project_dict,dataset= qds_dict)

        # now add ref to data model
        if join_features is not None:
            model_utils._create_dataset_relationship_from_dataset(project_dict=project_dict,
                                                                  cube_id=self.cube_id,
                                                                  dataset_name=dataset_name,
                                                                  join_features=join_features,
                                                                  join_columns=join_columns,
                                                                  roleplay_features=roleplay_features)

        self.project._update_project(project_json=project_dict,
                                     publish=publish)

    def write_feature_importance(self, dbconn: SQLConnection, table_name: str, dataframe: pd.DataFrame, feature_name_prefix: str,
                  folder: str = None, publish: bool = True, if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL):
        """Writes the dataframe with columns containing feature names and their importances to a table in the database accessed by dbconn with the given table_name.
        Then builds the created table into the data model so the importances can be queried.

        Args:
            dbconn (SQLConnection): connection to the database; should be the same one the model and project are based on
            table_name (str): the name for the table to be created for the given DataFrame
            dataframe (pd.DataFrame): the pandas DataFrame to write to the database
            feature_name_prefix (str): string to prepend to new feature names to make them easily identifiable
            folder (str): The folder to put the newly created items in. Defaults to None.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
            if_exists (PandasTableExistsActionType, optional): What to do if a table with table_name already exists. Defaults to PandasTableExistsActionType.FAIL.
        """
        model_utils._perspective_check(self)

        # verify our sql_connection is pointed at a connection that the model points at, and we'll use
        # that info later for join tables
        self._validate_warehouse_connection(dbconn)

        # this was commented out in atscale_comments - leaving commented for now until we get more info
        # check_multiple_features(join_features, self.get_all_categorical_features(),
        #                              errmsg='Make sure all items in join_features are categorical features')

        project_dict = self.project._get_dict()

        warehouse_id = project_parser.get_project_warehouse(project_dict)

        dbconn.write_df_to_db(table_name=table_name, dataframe=dataframe, if_exists=if_exists)
        database, schema = db_utils.get_database_and_schema(dbconn=dbconn)
        atscale_table_name = db_utils.get_atscale_tablename(atconn=self.project.atconn, warehouse_id=warehouse_id, database=database, schema=schema, table_name=table_name)

        column_dict = db_utils.get_column_dict(atconn=self.project.atconn, dbconn=dbconn,
                                               warehouse_id=warehouse_id, atscale_table_name=atscale_table_name, dataframe_columns=dataframe.columns)

        # If we're replacing a table, then the columns may have changed and the data sets need to be updated.
        if if_exists == PandasTableExistsActionType.REPLACE:
            self.project._update_project_tables([atscale_table_name], False)

        columns = self.project.atconn.get_table_columns(
            warehouse_id=warehouse_id, table_name=atscale_table_name, database=database, schema=schema)

        project_dataset, dataset_id = project_utils.create_dataset(
            atscale_table_name, warehouse_id, columns, database, schema)

        project_utils.add_dataset(project_dict, project_dataset)
        model_dict = model_utils._get_model_dict(self, project_dict)[0]
        model_utils._add_data_set_ref(model_dict, dataset_id)
        for column in dataframe.columns:
            name = column_dict[column]
            if dataframe[column].dtype.kind in 'iufc':
                feature_utils._create_aggregate_feature_local(
                    project_dict=project_dict, cube_id=self.cube_id, dataset_id=dataset_id, column_name=name, 
                    name=feature_name_prefix+'_feature_importance_'+column, folder=folder, aggregation_type=Aggs.SUM)
            else:
                dimension_utils.create_categorical_dimension_for_column(
                    project_dict=project_dict, cube_id=self.cube_id, dataset_id=dataset_id, column_name=name,
                    base_name=feature_name_prefix+'_feature_name', folder=folder)
    
        self.project._update_project(
            project_json=project_dict, publish=publish)

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
        model_utils._perspective_check(self)

        if join_columns is None:
            join_columns = join_features

        if len(join_features) != len(join_columns):
            raise atscale_errors.UserError(f'join_features and join_columns must be equal lengths. join_features is'
                                           f' length {len(join_features)} while join_columns is length {len(join_columns)}')

        # Verify the join_columns (which may be join_features now) are in the dataframe columns.
        # There was a method for this called check_multiple_features but this is a one-liner.
        # The check was commented out, but seems like a good one, so throwing it back in.
        for column in join_columns:
            if type(column) is list:
                for col in column:
                    if col not in dataframe.columns:
                        raise atscale_errors.UserError(
                            f'"{col}" in join_columns is not a column in the dataframe')
            else:
                if column not in dataframe.columns:
                    raise atscale_errors.UserError(
                        f'"{column}" in join_columns is not a column in the dataframe')

        # verify our sql_connection is pointed at a connection that the model points at, and we'll use
        # that info later for join tables
        self._validate_warehouse_connection(dbconn)

        # this was commented out in atscale_comments - leaving commented for now until we get more info
        # check_multiple_features(join_features, self.get_all_categorical_features(),
        #                              errmsg='Make sure all items in join_features are categorical features')
        df = dataframe.copy()
        project_dict = self.project._get_dict()
        key_dict = project_parser._get_feature_keys(project_dict, self.cube_id, join_features)

        joins = list(zip(join_features, join_columns))
        for i, (join_feature, join_column) in enumerate(joins):
            if type(join_column) is not list:
                join_column = [join_column]
                joins[i] = (join_feature, join_column)
            if len(join_column) != len(key_dict[join_feature]['key_cols']):
                raise atscale_errors.UserError(
                    f'Relationship for feature: "{join_feature}" '
                    f'requires multiple keys: "{key_dict[join_feature]["key_cols"]}" '
                    f'but received: "{join_column}"')
            if len(key_dict[join_feature]['key_cols']) == 1 and key_dict[join_feature]['key_cols'][0] != \
                key_dict[join_feature]['value_col']:
                df_key = db_utils._get_key_cols(dbconn, key_dict[join_feature])
                if df_key is not None:
                    if join_column[0] != key_dict[join_feature]['value_col']:
                        df_key.rename(columns={
                            key_dict[join_feature]['value_col']: join_column[0]}, inplace=True)
                    df = pd.merge(df, df_key, how='left', on=join_column[0])
                    joins[i] = (join_feature, [key_dict[join_feature]['key_cols'][0]])


        warehouse_id = project_parser.get_project_warehouse(project_dict)

        dbconn.write_df_to_db(table_name=table_name, dataframe=df, if_exists=if_exists)
        database, schema = db_utils.get_database_and_schema(dbconn=dbconn)
        atscale_table_name = db_utils.get_atscale_tablename(atconn=self.project.atconn, warehouse_id=warehouse_id, database=database, schema=schema, table_name=table_name)

        column_dict = db_utils.get_column_dict(atconn=self.project.atconn, dbconn=dbconn,
                                               warehouse_id=warehouse_id, atscale_table_name=atscale_table_name, dataframe_columns=df.columns)

        # If we're replacing a table, then the columns may have changed and the data sets need to be updated.
        if if_exists == PandasTableExistsActionType.REPLACE:
            self.project._update_project_tables([atscale_table_name], False)

        # Go through the join columns, which may be in a nested list if a relationship needs multiple keys
        # If the name of the key is in the dataframe we are all set, if not we use the column dict to map to the column name atscale sees
        atscale_join_columns = []
        for feature, columns in joins:
            nested_list = []
            for key, column in zip(key_dict[feature]['key_cols'], columns):
                if key in df.columns:
                    nested_list.append(key)
                else:
                    nested_list.append(column_dict[column])
            atscale_join_columns.append(nested_list)

        database, schema = db_utils.get_database_and_schema(dbconn=dbconn)
        # create_dataset_relationship now mutates the project_json and returns, then we're responsible for posting
        project_dict = model_utils._create_dataset_relationship(atconn=self.project.atconn, project_dict=project_dict, cube_id=self.cube_id,
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
        model_utils._perspective_check(self)

        project_dict = model_utils._create_dataset_relationship(atconn=self.project.atconn, project_dict=self.project._get_dict(), cube_id=self.cube_id,
                                                                database=database, schema=schema, table_name=table_name, join_features=join_features, join_columns=join_columns, roleplay_features=roleplay_features)

        self.project._update_project(
            project_json=project_dict, publish=publish)

    def create_dataset_relationship(self, dataset_name: str, join_features: List[str], join_columns: List[str] = None, roleplay_features: List[str] = None, publish: bool = True):
        """Creates a relationship between a dataset and features in the model

        Args:
            dataset_name (str): The dataset to join
            join_features (List[str]): The features in the data model to join on
            join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
                None or the same length and order as join_features. Defaults to None to use identical names to the
                join_features. If multiple columns are needed for a single join they should be in a nested list
            roleplay_features (List[str], optional): The roleplays to use on the relationships. List must be either
                None or the same length and order as join_features. Use '' to not roleplay that relationship. Defaults to None.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)
        
        original_project_dict = self.project._get_dict()
        if not project_parser.get_dataset_from_datasets_by_name(
            project_parser.get_datasets(original_project_dict), dataset_name):
            raise atscale_errors.UserError(
                    f'No dataset with the name {dataset_name} found in project')
        project_dict = model_utils.create_dataset_relationship_from_dataset(project_dict=original_project_dict, cube_id=self.cube_id,
                                                               dataset_name=dataset_name, join_features=join_features, join_columns=join_columns, roleplay_features=roleplay_features)
        self.project._update_project(project_json=project_dict, publish=publish)

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
        # set use_aggs and gen_aggs to True because we set them in the json when using the api 
        # and this stops the flags being commented into the query
        query = query_utils._generate_atscale_query(data_model=self, feature_list=feature_list,
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

        queryResponse = self.project.atconn._post_atscale_query(query, self.project.project_name, use_aggs=use_aggs,
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
        return dbconn.submit_query(
            query_utils.generate_db_query(data_model=self,
                              atscale_query=query_utils._generate_atscale_query(
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
        query = query_utils._generate_atscale_query(data_model=self, feature_list=feature_list,
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
        try:
            from pyspark.sql import SparkSession
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError('spark', str(e))

        query = query_utils.generate_db_query(self, query_utils._generate_atscale_query(data_model=self,
                                                feature_list=feature_list,
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

        # we cannot support jdbc query to databricks data warehouses right now due to issues on the databricks side.
        # databricks can serve as the spark evironment you query from however. 
        connected_warehouses = self.project.atconn.get_connected_warehouses()
        warehouse_in_use = project_parser.get_project_warehouse(self.project._get_dict())
        our_warehouse = [warehouse for warehouse in connected_warehouses if warehouse['warehouse_id'] == warehouse_in_use][0]

        if our_warehouse['platform'] in ['databrickssql', 'databricks']:
            raise atscale_errors.UserError('This function is not currently supported for Databricks Warehouses due to '/
            'an error with connecting to Databricks via jdbc. If you are attempting to query a databricks warehouse from '/
            'within a databricks notebook, get_data_spark_from_spark may be an alternative.')

        df = sparkSession.read.format(jdbc_format).options(**jdbc_options) \
                        .option("query", query).load()

        column_index = range(len(df.columns))
        column_names = df.columns

        for column in column_index:
            df = df.withColumnRenamed(column_names[column], feature_list[column])

        return df

    def get_data_spark_from_spark(self, feature_list: List[str], dbconn: SQLConnection, spark_session,
                 filter_equals: Dict[str, str] = None, filter_greater: Dict[str, str] = None,
                 filter_less: Dict[str, str] = None, filter_greater_or_equal: Dict[str, str] = None,
                 filter_less_or_equal: Dict[str, str] = None, filter_not_equal: Dict[str, str] = None,
                 filter_in: Dict[str, list] = None, filter_between: Dict[str, tuple] = None,
                 filter_like: Dict[str, str] = None, filter_rlike: Dict[str, str] = None,
                 filter_null: List[str] = None, filter_not_null: List[str] = None, limit: int = None,
                 comment: str = None, use_aggs=True, gen_aggs=True):
        """Uses the provided sparkSession to execute a query generated by the atscale query engine. 
        Returns the results in a spark DataFrame.

        Args:
            feature_list (List[str]): The list of features to query.
            dbconn (SQLConnection): connection to the database; should be the same one the model and project are based on
            spark_session (pyspark.sql.SparkSession): The pyspark SparkSession to execute the query with
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
        try:
            from pyspark.sql import SparkSession
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError('spark', str(e))

        query = query_utils.generate_db_query(self, query_utils._generate_atscale_query(data_model=self,
                                                feature_list=feature_list,
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

        #ok here I want to call a sqlconn function that optionally can adjust the default catalog/database of the session and then revert it
        df = dbconn._read_pysparkdf_from_spark_db(spark_session = spark_session, query= query)

        column_index = range(len(df.columns))
        column_names = df.columns

        for column in column_index:
            df = df.withColumnRenamed(column_names[column], feature_list[column])

        return df

    def get_database_query(self, feature_list, filter_equals=None, filter_greater=None, filter_less=None,
                           filter_greater_or_equal=None, filter_less_or_equal=None, filter_not_equal=None, filter_in=None,
                           filter_between=None, filter_like=None, filter_rlike=None, filter_null=None, filter_not_null=None, limit=None,
                           comment=None, use_aggs=True, gen_aggs=True) -> str:
        """Returns a database query generated using the AtScale model to get the given features

        Args:
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
            str: The generated database query
        """
        return query_utils.generate_db_query(data_model=self,
                                  atscale_query=query_utils._generate_atscale_query(
                                  data_model=self,
                                  feature_list=feature_list, filter_equals=filter_equals, filter_greater=filter_greater,
                                  filter_less=filter_less, filter_greater_or_equal=filter_greater_or_equal,
                                  filter_less_or_equal=filter_less_or_equal, filter_not_equal=filter_not_equal,
                                  filter_in=filter_in, filter_between=filter_between, filter_like=filter_like,
                                  filter_rlike=filter_rlike, filter_null=filter_null, filter_not_null=filter_not_null,
                                  limit=limit, comment=comment),use_aggs=use_aggs,gen_aggs=gen_aggs)
    
    

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
        model_utils._perspective_check(self)

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
        # self._validate_warehouse_connection(dbconn)


        warehouse_id = project_parser.get_project_warehouse(
            self.project._get_dict())

        dbconn._write_pysparkdf_to_external_db(pyspark_dataframe= pyspark_dataframe, jdbc_format= jdbc_format, jdbc_options= jdbc_options, 
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

        project_dict = self.project._get_dict()
        key_dict = project_parser._get_feature_keys(project_dict, self.cube_id, join_features)

        joins = list(zip(join_features, join_columns))
        for i, (join_feature, join_column) in enumerate(joins):
            if type(join_column) is not list:
                join_column = [join_column]
                joins[i] = (join_feature, join_column)
            if len(join_column) != len(key_dict[join_feature]['key_cols']):
                raise atscale_errors.UserError(
                    f'Relationship for feature: "{join_feature}" '
                    f'requires multiple keys: "{key_dict[join_feature]["key_cols"]}" '
                    f'but received: "{join_column}"')
            if len(key_dict[join_feature]['key_cols']) == 1 and key_dict[join_feature]['key_cols'][0] != \
                key_dict[join_feature]['value_col']:
                df_key = db_utils._get_key_cols(dbconn, key_dict[join_feature])
                if df_key is not None:
                    if join_column[0] != key_dict[join_feature]['value_col']:
                        df_key.rename(columns={
                            key_dict[join_feature]['value_col']: join_column[0]}, inplace=True)
                    df = pd.merge(df, df_key, how='left', on=join_column[0])
                    joins[i] = (join_feature, [key_dict[join_feature]['key_cols'][0]])

        # TODO: connect with John Lynch and potentially rethink this code. Some SQLConnection
        # implementations do not have a database or schema variable to even call and see if it's None.
        # So for now I'll just determine if they even have that attribute with introspection in addition
        # to checking it's value, but seems like there may be a smoother approach. Also not sure what
        # will happen in join_table below which currently requires a schema value
        database, schema = db_utils.get_database_and_schema(dbconn=dbconn)

        # join_table now mutates the project_json and returns, then we're responsible for posting
        project_dict = model_utils._create_dataset_relationship(atconn=self.project.atconn,
                                                                project_dict=self.project._get_dict(),
                                                                cube_id=self.cube_id,
                                     database=database, schema=schema, table_name=atscale_table_name, join_features=join_features, join_columns=atscale_join_columns, roleplay_features=roleplay_features)

        self.project._update_project(
            project_json=project_dict, publish=publish)

    def writeback_spark_to_spark(self, dbconn: SQLConnection, pyspark_dataframe, join_features: list, 
                  table_name: str = None, alt_database_path: str = None, join_columns: list = None, roleplay_features: list = None,
                  publish: bool = True, if_exists: PysparkTableExistsActionType = PysparkTableExistsActionType.ERROR):
        """Writes the pyspark dataframe to a table in the database accessed via jdbc with the given table_name. Joins that table to this
        DataModel by joining on the given join_features or join_columns. 

        Args:
            dbconn (SQLConnection): connection to the database; should be the same one the model and project are based on
            pyspark_dataframe (pyspark.sql.DataFrame): The pyspark dataframe to write
            join_features (list): a list of features in the data model to use for joining.
            table_name (str, optional): The name for the table to be created for the given PySpark DataFrame. Can be none if name specified in options
            alt_database_path (str, optional): The alternate database path to use. Will be added as a prefix to the tablename. 
                Defaults to None, and uses the default database if None. Include the trailing delimiter to go between path and tablename.
            join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
                None or the same length and order as join_features. Defaults to None to use identical names to the
                join_features. If multiple columns are needed for a single join they should be in a nested list
            roleplay_features (list, optional): The roleplays to use on the relationships. List must be either
                None or the same length and order as join_features. Use '' to not roleplay that relationship. Defaults to None.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
            if_exists (PysparkTableExistsActionType, optional): What to do if a table with table_name already exists. Defaults to PysparkTableExistsActionType.ERROR.
        """
        model_utils._perspective_check(self)

        #import the needed spark packages
        try:
            from pyspark.sql import DataFrame
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError('spark', str(e))

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
        # self._validate_warehouse_connection(dbconn)


        warehouse_id = project_parser.get_project_warehouse(
            self.project._get_dict())

        dbconn._write_pysparkdf_to_spark_db(pyspark_dataframe= pyspark_dataframe, alt_database_path= alt_database_path, 
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
        project_dict = self.project._get_dict()
        key_dict = project_parser._get_feature_keys(project_dict, self.cube_id, join_features)

        joins = list(zip(join_features, join_columns))
        for i, (join_feature, join_column) in enumerate(joins):
            if type(join_column) is not list:
                join_column = [join_column]
                joins[i] = (join_feature, join_column)
            if len(join_column) != len(key_dict[join_feature]['key_cols']):
                raise atscale_errors.UserError(
                    f'Relationship for feature: "{join_feature}" '
                    f'requires multiple keys: "{key_dict[join_feature]["key_cols"]}" '
                    f'but received: "{join_column}"')
            if len(key_dict[join_feature]['key_cols']) == 1 and key_dict[join_feature]['key_cols'][0] != \
                key_dict[join_feature]['value_col']:
                df_key = db_utils._get_key_cols(dbconn, key_dict[join_feature])
                if df_key is not None:
                    if join_column[0] != key_dict[join_feature]['value_col']:
                        df_key.rename(columns={
                            key_dict[join_feature]['value_col']: join_column[0]}, inplace=True)
                    df = pd.merge(df, df_key, how='left', on=join_column[0])
                    joins[i] = (join_feature, [key_dict[join_feature]['key_cols'][0]])
        # TODO: connect with John Lynch and potentially rethink this code. Some SQLConnection
        # implementations do not have a database or schema variable to even call and see if it's None.
        # So for now I'll just determine if they even have that attribute with introspection in addition
        # to checking it's value, but seems like there may be a smoother approach. Also not sure what
        # will happen in join_table below which currently requires a schema value
        database, schema = db_utils.get_database_and_schema(dbconn=dbconn)

        # join_table now mutates the project_json and returns, then we're responsible for posting
        project_dict = model_utils._create_dataset_relationship(atconn=self.project.atconn,
                                                                project_dict=self.project._get_dict(),
                                                                cube_id=self.cube_id,
                                                                database=database, schema=schema,
                                                                table_name=atscale_table_name,
                                                                join_features=join_features,
                                                                join_columns=atscale_join_columns,
                                                                roleplay_features=roleplay_features)

        self.project._update_project(
            project_json=project_dict, publish=publish)

    def _validate_warehouse_connection(self, dbconn: SQLConnection)->bool:
        project_datasets = self._get_referenced_project_datasets()
        connections = self.project.atconn._get_connection_groups()
        project_connections = project_parser.get_connection_list_for_project_datasets(
            project_datasets, connections)
        for project_connection in project_connections:
            if dbconn._verify(project_connection):
                return True
        msg = 'The SQLConnection connects to a database that is not referenced by the given data_model.'
        logger.exception(msg)
        raise atscale_errors.UserError(msg)

    def create_secondary_attribute(self, dataset_name: str, column_name: str, new_attribute_name: str, hierarchy_name: str, level_name: str,
                               description: str = None, caption: str = None, folder: str = None, visible: bool = True, publish: bool = True):
        """Creates a new secondary attribute on an existing hierarchy and level.

        Args:
            dataset_name (str): The dataset containing the column that the feature will use.
            column_name (str): The column that the feature will use.
            new_attribute_name (str): What the attribute will be called.
            hierarchy_name (str): What hierarchy to add the attribute to.
            level_name (str): What level of the hierarchy to add the attribute to.
            description (str, optional): The description for the attribute. Defaults to None.
            caption (str, optional): The caption for the attribute. Defaults to None.
            folder (str, optional): The folder for the attribute. Defaults to None.
            visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to True.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        project_json = self.project._get_dict()

        if new_attribute_name in list(self.get_features().keys()):
            raise atscale_errors.UserError(
                f'Invalid name: \'{new_attribute_name}\'. A feature already exists with that name')
         
        if not self.dataset_exists(dataset_name):
            raise atscale_errors.UserError(
                f'Dataset \'{dataset_name}\' not associated with given model')

        if not model_utils._column_exists(project_json, dataset_name, column_name):
            raise atscale_errors.UserError(
                f'Column \'{column_name}\' not found in the \'{dataset_name}\' dataset')

        feature_utils._check_unpublished_hierarchy(project_json, self.name, hierarchy_name, level_name, expect_base_input= True)

        data_set = project_parser.get_dataset_from_datasets_by_name(project_parser.get_datasets(project_json),
                                                            dataset_name)

        #call the helper
        feature_utils._create_secondary_attribute(self, project_json, data_set, column_name= column_name, 
            new_attribute_name= new_attribute_name, hierarchy_name=hierarchy_name, level_name= level_name, description= description,
            caption= caption, folder= folder, visible=visible)

        self.project._update_project(
            project_json=project_json, publish=publish)  

    def update_secondary_attribute(self, attribute_name: str, description: str = None, caption: str = None,
                                        folder: str = None, publish: bool = True):
        """Updates the metadata for an existing secondary attribute.

        Args:
            attribute_name (str): The name of the feature to update.
            description (str, optional): The description for the feature. Defaults to None to leave unchanged.
            caption (str, optional): The caption for the feature. Defaults to None to leave unchanged.
            folder (str, optional): The folder to put the feature in. Defaults to None to leave unchanged.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        project_json = self.project._get_dict()
        # TODO update this to use _get_unpublished_hierarchies once created
        filter_by = {Hierarchy.secondary_attribute: [True], Hierarchy.name: [attribute_name]}
        secondary_attributes = metadata_utils._get_hierarchies(self, filter_by= filter_by)
        attributes = [x for x in project_json.get('attributes', {}).get('keyed-attribute', []) if x['name'] == attribute_name]
        if len(attributes) < 1:
            if secondary_attributes.get(attribute_name, False):
                raise Exception(f'Secondary Attribute: {attribute_name} is roleplayed but only the base name can be used to update metadata.')
            else:
                raise Exception(f'Secondary Attribute: {attribute_name} does not exist.')
        feature_utils._update_secondary_attribute(project_dict=project_json, attribute_name= 
                                                    attribute_name, description= description, caption= caption,
                                                    folder= folder)
        if project_json is not None:
            self.project._update_project(
                project_json=project_json, publish=publish)  
        
    def create_filter_attribute(self, new_feature_name: str, level_name: str, hierarchy_name: str, filter_values: List[str],
                            caption: str = None, description: str = None,
                            folder: str = None, visible: str = True, publish: bool = True):
        """Creates a new boolean secondary attribute to filter on a given subset of the level's values.

        Args:
            new_feature_name (str): The name of the new feature.
            level_name (str): The name of the level to apply the filter to.
            hierarchy_name (str): The hierarchy the level belongs to.
            filter_values (List[str]): The list of values to filter on.
            caption (str): The caption for the feature. Defaults to None.
            description (str): The description for the feature. Defaults to None.
            folder (str): The folder to put the feature in. Defaults to None.
            visible (bool): Whether the created attribute will be visible to BI tools. Defaults to True.
            publish (bool): Whether or not the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        project_dict = self.project._get_dict()

        if new_feature_name in list(self.get_features().keys()):
            raise atscale_errors.UserError(
                f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')
        
        feature_utils._check_unpublished_hierarchy(project_dict, self.name, hierarchy_name, level_name, expect_base_input= True)

        feature_utils._create_filter_attribute(self, project_dict=project_dict, new_feature_name=new_feature_name,
                                               level_name=level_name, hierarchy_name=hierarchy_name,
                                               filter_values=filter_values, caption=caption, description=description,
                                               folder=folder, visible=visible)
        self.project._update_project(
                project_json=project_dict, publish=publish)  

    def create_mapped_columns(self, dataset_name: str, column_name: str, mapped_names: List[str], data_types: List[MappedColumnDataTypes],
                          key_terminator: MappedColumnKeyTerminator, field_terminator: MappedColumnFieldTerminator,
                          map_key_type: MappedColumnDataTypes, map_value_type: MappedColumnDataTypes, first_char_delimited: bool = False,
                          publish: bool = True):
        """Creates a mapped column.  Maps a column that is a key value structure into one or more new columns with the
        name of the given key(s). Types for the source keys and columns, and new columns are required. Valid types include
        'Int', 'Long', 'Boolean', 'String', 'Float', 'Double', 'Decimal', 'DateTime', and 'Date'.

        Args:
            dataset_name (str): The dataset the mapped column will be derived in.
            column_name (str): The name of the column.
            mapped_names (list str): The names of the mapped columns.
            data_types (list MappedColumnDataTypes): The types of the mapped columns.
            key_terminator (MappedColumnKeyTerminator): The key terminator. Valid values are ':', '=', and '^'
            field_terminator (MappedColumnFieldTerminator): The field terminator. Valid values are ',', ';', and '|'
            map_key_type (MappedColumnDataTypes): The mapping key type for all the keys in the origin column.
            map_value_type (MappedColumnDataTypes): The mapping value type for all values in the origin column.
            first_char_delimited (bool): Whether the first character is delimited. Defaults to False.
            publish (bool): Whether the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        project_dict = self.project._get_dict()

        dset = project_parser.get_dataset_from_datasets_by_name(
            project_datasets=project_parser.get_datasets(project_dict),
            dataset_name=dataset_name)
        if not dset:
            raise atscale_errors.UserError(f'Invalid parameter: dataset name {dataset_name} does not exist')
        if project_utils._check_if_qds(dset):
            raise atscale_errors.UserError(f'Invalid parameter: dataset name {dataset_name} is a qds and cannot have '
                                           f'calculated columns')

        dset['physical'].setdefault('columns', [])
        dset_columns = [c['name'] for c in dset['physical']['columns']]

        model_utils._check_features(features=[column_name],
                    check_list=dset_columns,
                    errmsg=f'Invalid parameter: column name \'{column_name}\' does not exist in'
                            f' dataset \'{dataset_name}\'')

        
        feature_utils._create_mapped_columns(dataset= dset, column_name= column_name, mapped_names= mapped_names,
                          data_types = data_types, key_terminator= key_terminator, field_terminator = field_terminator,
                          map_key_type= map_key_type, map_value_type = map_value_type, first_char_delimited = first_char_delimited)

        self.project._update_project(
            project_json=project_dict, publish=publish)

    def add_column_mapping(self, dataset_name: str, column_name: str, mapped_name: str, data_type: MappedColumnDataTypes, publish: bool = True):
        """Adds a new mapping to an existing column mapping

        Args:
            dataset_name (str): The dataset the mapping belongs to.
            column_name (str): The column the mapping belongs to.
            mapped_name (MappedColumnDataTypes): The name for the new mapped column.
            data_type (str): The data type of the new mapped column.
            publish (bool, optional): _description_. Defaults to True.
        """
        model_utils._perspective_check(self)

        project_dict = self.project._get_dict()
        
        if not self.dataset_exists(dataset_name):
            raise atscale_errors.UserError(
                f'Dataset \'{dataset_name}\' not associated with given model')

        if not model_utils._column_exists(project_dict, dataset_name, column_name):
            raise atscale_errors.UserError(
                f'Column \'{column_name}\' not found in the \'{dataset_name}\' dataset')

        dset = project_parser.get_dataset_from_datasets_by_name(
            project_datasets=project_parser.get_datasets(project_dict),
            dataset_name=dataset_name)

        if 'map-column' not in dset['physical']:
            raise atscale_errors.UserError(
                f'No mapped column exists in the dataset. Use create_mapped_columns to create one')
        
        mapping_cols = [c for c in dset['physical']
                        ['map-column'] if c['name'] == column_name]
        if len(mapping_cols) < 1:
            raise atscale_errors.UserError(f'No mapped column exists for column: {mapped_name}. Use create_mapped_columns '
                                        f'to create one')

        already_mapped_w_name = [col for col in mapping_cols[0]
                                ['columns']['columns'] if col['name'] == mapped_name]
        if already_mapped_w_name:
            raise atscale_errors.UserError(
                f'There is already a mapping on column \'{column_name}\' for the key \'{mapped_name}\'')
        # todo: raise error if mapping conflicts with normal column?

        feature_utils._add_column_mapping(dataset=dset, column_name= column_name, mapped_name= mapped_name,
            data_type= data_type)

        self.project._update_project(
            project_json=project_dict, publish=publish)

    def create_calculated_column(self, dataset_name: str, column_name: str, expression: str, publish: bool = True):
        """Creates a new calculated column. A calculated column is a column whose value is calculated by a SQL
        expression (referencing one or more columns from the dataset) run at query time for each row.
        See AtScale documentation for more info on calculated columns.

        Args:
            dataset_name (str): The dataset the calculated column will be derived in.
            column_name (str): The name of the column.
            expression (str): The SQL expression for the column.
            publish (bool): Whether the updated project should be published. Defaults to True.

        Raises:
            atscale_errors.UserError: If the given dataset or column does not exist in the data model
        """
        model_utils._perspective_check(self)
        project_dict = self.project._get_dict()

        dset = project_parser.get_dataset_from_datasets_by_name(
            project_datasets=project_parser.get_datasets(project_dict),
            dataset_name=dataset_name)
        if not dset:
            raise atscale_errors.UserError(f'Invalid parameter: dataset name {dataset_name} does not exist')
        if model_utils._column_exists(project_dict=project_dict, dataset_name=dataset_name, column_name=column_name):
            raise atscale_errors.UserError(f'Invalid parameter: column_name {column_name} already exists in the given '
                                           f'dataset')
        if project_utils._check_if_qds(dset):
            raise atscale_errors.UserError(f'Invalid parameter: dataset name {dataset_name} is a qds and cannot have '
                                           f'calculated columns')

        project_utils.add_calculated_column_to_project_dataset(atconn=self.project.atconn,
                                                               data_set=dset,
                                                               column_name=column_name,
                                                               expression=expression)
        self.project._update_project(project_json=project_dict, publish=publish)

    def create_calculated_feature(self, new_feature_name: str, expression: str, description: str = None,
                                caption: str = None, folder: str = None,
                                format_string: Union[FeatureFormattingType, str] = None, visible: bool = True,
                                publish: bool = True):
        """Creates a new calculated feature given a name and an MDX Expression.

        Args:
            new_feature_name (str): What the feature will be called.
            expression (str): The MDX expression for the feature.
            description (str): The description for the feature. Defaults to None.
            caption (str): The caption for the feature. Defaults to None.
            folder (str): The folder to put the feature in. Defaults to None.
            format_string (str): The format string for the feature. Defaults to None.
            visible (bool): Whether the feature will be visible to BI tools. Defaults to True.
            publish (bool): Whether the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)
        if new_feature_name in list(self.get_features().keys()):
            raise atscale_errors.UserError(
                f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')

        project_json = self.project._get_dict()
        feature_utils._create_calculated_feature_local(project_dict=project_json,
                                        cube_id=self.cube_id,
                                        name=new_feature_name,
                                        expression=expression,
                                        description=description,
                                        caption=caption,
                                        folder=folder,
                                        format_string=format_string,
                                        visible=visible)

        self.project._update_project(
            project_json=project_json, publish=publish)

    def update_calculated_feature(self, feature_name: str, expression: str = None, description: str = None, caption: str = None,
                              folder: str = None, format_string: Union[FeatureFormattingType, str] = None,
                              visible: bool = None, publish: bool = True):
        """Update the metadata for a calculated feature.

        Args:
            feature_name (str): The name of the feature to update.
            expression (str): The expression for the feature. Defaults to None to leave unchanged.
            description (str): The description for the feature. Defaults to None to leave unchanged.
            caption (str): The caption for the feature. Defaults to None to leave unchanged.
            folder (str): The folder to put the feature in. Defaults to None to leave unchanged.
            format_string (str): The format string for the feature. Defaults to None to leave unchanged.
            visible (bool): Whether the updated feature should be visible. Defaults to None to leave unchanged.
            publish (bool): Whether the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        calculated_measure_matches = get_dmv_data(self, [Measure.type], filter_by={
            Measure.type: ['Calculated'],
            Measure.name: [feature_name]})

        if not len(calculated_measure_matches):
            raise atscale_errors.UserError(
                f'Invalid name: \'{feature_name}\'. A feature with that name does not exist')

        project_dict = self.project._get_dict()

        feature_utils._update_calculated_feature(project_dict=project_dict, feature_name=feature_name, expression= expression, 
                                    description= description, caption= caption, folder=folder,
                                    format_string=format_string, visible= visible)
        self.project._update_project(
            project_json=project_dict, publish=publish)

    def create_denormalized_categorical_feature(self, dataset_name: str, column_name: str, name: str, description: str = None,
                                                caption: str = None, folder: str = None, visible: bool = True, publish: bool = True):
        """Creates a new denormalized categorical feature.

        Args:
            dataset_name (str): The name of the dataset to find the column_name.
            column_name (str): The column that the feature will use.
            name (str): What the feature will be called.
            description (str, optional): The description for the feature. Defaults to None.
            caption (str, optional): The caption for the feature. Defaults to None.
            folder (str, optional): The folder to put the feature in. Defaults to None.
            visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to True.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        if name in list(self.get_features().keys()):
            raise atscale_errors.UserError(
                f'Invalid name: \'{name}\'. A feature already exists with that name')

        project_dict = self.project._get_dict() 
        if not model_utils._fact_dataset_exists(self, project_dict, dataset_name=dataset_name):
            raise atscale_errors.UserError(
                f'Dataset \'{dataset_name}\' not associated with given model')

        if not model_utils._column_exists(project_dict, dataset_name, column_name):
            raise atscale_errors.UserError(
                f'Column \'{column_name}\' not found in the \'{dataset_name}\' dataset')

        data_set_project = project_parser.get_dataset_from_datasets_by_name(project_parser.get_datasets(project_dict),
                                                                            dataset_name)
        dataset_id = data_set_project.get('id')
        dimension_utils.create_categorical_dimension_for_column(project_dict=project_dict, cube_id=self.cube_id, dataset_id=dataset_id,
                                                                column_name=column_name, base_name=name, description=description, caption=caption, folder=folder, visible=visible)
        self.project._update_project(
            project_json=project_dict, publish=publish)

    def create_aggregate_feature(self, dataset_name: str, column_name: str, name: str, aggregation_type: Aggs,
                                description: str = None, caption: str = None, folder: str = None,
                                format_string: Union[FeatureFormattingType, str] = None, visible: bool = True, publish: bool = True):
        """Creates a new aggregate feature.

        Args:
            dataset_name (str): The dataset containing the column that the feature will use.
            column_name (str): The column that the feature will use.
            name (str): What the feature will be called.
            aggregation_type (atscale.utils.enums.Aggs): What aggregation method to use for the feature. Example: Aggs.MAX
                Valid options can be found in utils.Aggs
            description (str): The description for the feature. Defaults to None.
            caption (str): The caption for the feature. Defaults to None.
            folder (str): The folder to put the feature in. Defaults to None.
            format_string: The format string for the feature. Defaults to None.
            visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to True.
            publish (bool): Whether or not the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        if name in list(self.get_features().keys()):
            raise atscale_errors.UserError(
                f'Invalid name: \'{name}\'. A feature already exists with that name')
      
        project_dict = self.project._get_dict() 
        if not model_utils._fact_dataset_exists(self, project_dict, dataset_name=dataset_name):
            raise atscale_errors.UserError(
                f'Dataset \'{dataset_name}\' not associated with given model')

        if not model_utils._column_exists(project_dict, dataset_name, column_name):
            raise atscale_errors.UserError(
                f'Column \'{column_name}\' not found in the \'{dataset_name}\' dataset')
    
        project_dict = self.project._get_dict()
        dataset_id = project_parser.get_dataset_from_datasets_by_name(
            project_parser.get_datasets(project_dict), dataset_name)['id']
            
        feature_utils._create_aggregate_feature_local(project_dict=project_dict, 
                                        cube_id= self.cube_id, 
                                        dataset_id=dataset_id,
                                        column_name=column_name, name= name,
                                        aggregation_type=aggregation_type, 
                                        description=description, caption=caption, 
                                        folder=folder, format_string=format_string, 
                                        visible=visible)
        
        self.project._update_project(
            project_json=project_dict, publish=publish)

    def update_aggregate_feature(self, feature_name: str, description: str = None, caption: str = None,
                                      folder: str = None,
                                      format_string: Union[FeatureFormattingType, str] = None,
                                      visible: bool = None, publish: bool = True):
        """Update the metadata for an aggregate feature.

        Args:
            feature_name (str): The name of the feature to update.
            description (str): The description for the feature. Defaults to None to leave unchanged.
            caption (str): The caption for the feature. Defaults to None to leave unchanged.
            folder (str): The folder to put the feature in. Defaults to None to leave unchanged.
            format_string (str): The format string for the feature. Defaults to None to leave unchanged.
            visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to None to leave unchanged.
            publish (bool): Whether the updated project should be published. Defaults to True.

        Raises:
            atscale_error.UserError: If the given name does not exist in the data model.
        """
        model_utils._perspective_check(self)

        agg_feature_matches = get_dmv_data(self, [Measure.type], filter_by={
            Measure.type: ['Aggregate'],
            Measure.name: [feature_name]})

        if not agg_feature_matches:
            raise atscale_errors.UserError(
                f'Invalid name: \'{feature_name}\'. A feature with that name does not exist')

        project_json = self.project._get_dict()

        feature_utils._update_aggregate_feature(project_dict= project_json, cube_id= self.cube_id, 
                                    feature_name= feature_name, description= description, 
                                    caption= caption, folder= folder, format_string= format_string,
                                    visible=visible)

        self.project._update_project(
            project_json=project_json, publish=publish)

    def create_rolling_features(self, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str,
                        level_name: str, aggregation_types: List[MDXAggs] = None, description: str = None, caption: str = None, folder: str = None,
                        format_string: str = None, visible: bool = True, publish: bool = True) -> str:
        """Creates a rolling calculated numeric feature for the given column. If no list of MDXAggs is provided, rolling calc features
            will be made for Sum, Mean, Min, Max, and Stdev 

        Args:
            new_feature_name (str): What the feature will be called, will be suffixed with the agg type if multiple are 
                being created.
            numeric_feature_name (str): The numeric feature to use for the calculation
            time_length (int): The length of time the feature should be calculated over
            hierarchy_name (str): The time hierarchy used in the calculation
            level_name (str): The level within the time hierarchy
            aggregation_types (List[MDXAggs], optional): The type of aggregation to do for the rolling calc. If none, all agg
                types are used. 
            description (str, optional): The description for the feature. Defaults to None.
            caption (str, optional): The caption for the feature. Defaults to None.
            folder (str, optional): The folder to put the feature in. Defaults to None.
            format_string (str, optional): The format string for the feature. Defaults to None.
            visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.)
            
        Returns:
            str: A message stating that the feature was successfully created
        """
        model_utils._perspective_check(self)

        if not (type(time_length) == int) or time_length < 1:
            raise atscale_errors.UserError(
                f'Invalid parameter value \'{time_length}\', Length must be an integer greater than zero')


        model_utils._check_features([numeric_feature_name], list(self.get_features().keys()),
                   errmsg=f'Make sure \'{numeric_feature_name}\' is a numeric feature')

        #make sure the input is a list
        if aggregation_types is None:
            aggregation_types = [x for x in MDXAggs]
        
        if type(aggregation_types) != list:
            aggregation_types = [aggregation_types]

        #validate that the columns we are about to make don't already exist.
        measure_list = list(get_dmv_data(
            model=self, id_field=Measure.name).keys())
        if len(aggregation_types) > 1:
            new_feature_names = [new_feature_name+'_'+x.name for x in aggregation_types]
        else: new_feature_names = [new_feature_name]
        
        for name in new_feature_names:
            if name in measure_list:
                raise atscale_errors.UserError(
                    f'Invalid name: The column about to be created, \'{name}\', already exists in the model')

        hier_dict, level_dict = feature_utils._check_time_hierarchy(data_model=self,
                                                    hierarchy_name=hierarchy_name,
                                                    level_name=level_name)

        time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]

        project_json = self.project._get_dict()
        for i in range(len(aggregation_types)):
            aggregation_type = aggregation_types[i]
            feat_name = new_feature_names[i]

            feature_utils._create_rolling_agg(project_json, cube_id= self.cube_id, time_dimension= time_dimension, agg_type=aggregation_type,
                                                new_feature_name= feat_name, numeric_feature_name= numeric_feature_name,
                                                time_length=time_length, hierarchy_name= hierarchy_name, 
                                                level_name= level_name, description=description, caption= caption,
                                                folder= folder, format_string= format_string, visible= visible)

        self.project._update_project(
            project_json=project_json, publish=publish)

        new_feature_names_string = ', '.join(new_feature_names)
        return f'Successfully created measures \'{new_feature_names_string}\' {f"in folder {folder}" if folder else ""}' 

    def create_lag_feature(self, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str, level_name: str,
                description: str = None, caption: str = None, folder: str = None, format_string: str = None, visible: bool = True,
                publish: bool = True):
        """Creates a lagged feature based on the numeric feature and time hierachy passed in.

        Args:
            new_feature_name (str): The name of the feature to create.
            numeric_feature_name (str): The numeric feature to lag.
            time_length (int): The length of the lag.
            hierarchy_name (str): The time hierarchy to use for the lag.
            level_name (str): The level of the hierarchy to use for the lag.
            description (str, optional): A description for the feature. Defaults to None.
            caption (str, optional): A caption for the feature. Defaults to None.
            folder (str, optional): The folder to put the feature in. Defaults to None.
            format_string (str, optional): A format sting for the feature. Defaults to None.
            visible (bool, optional): Whether the feature should be visible. Defaults to True.
            publish (bool, optional): Whether to publish the project after creating the feature. Defaults to True.
        """
        model_utils._perspective_check(self)

        model_utils._check_features(features=[numeric_feature_name],
                    check_list=list(get_dmv_data(model=self, fields=[],
                                                    id_field=Measure.name,
                                                    filter_by={
                                                        Measure.name: [numeric_feature_name]}).keys()),
                    errmsg=f'Invalid parameter value \'{numeric_feature_name}\' is not a numeric feature in the data model')

        if new_feature_name in list(self.get_features().keys()):
            raise atscale_errors.UserError(
                f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')
   
        if not (type(time_length) == int) or time_length <= 0:
            raise atscale_errors.UserError(
                f'Invalid parameter value \'{time_length}\', Length must be an integer greater than zero')

        hier_dict, level_dict = feature_utils._check_time_hierarchy(data_model=self, 
                                                    hierarchy_name=hierarchy_name, level_name=level_name)

        time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]

        #the project dict that will be edited by the operation
        project_json = self.project._get_dict()

        feature_utils._create_lag_feature_local(project_dict= project_json, cube_id= self.cube_id,
                                time_dimension= time_dimension, new_feature_name = new_feature_name, 
                                numeric_feature_name= numeric_feature_name,time_length = time_length, 
                                hierarchy_name = hierarchy_name, level_name = level_name, 
                                description=description, caption=caption, folder=folder,
                                format_string=format_string, visible=visible)
        self.project._update_project(
            project_json=project_json, publish=publish)

    def create_time_differencing_feature(self, new_feature_name: str, numeric_feature_name: str, time_length: int,
                                hierarchy_name: str, level_name: str, description: str = None, caption: str = None,
                                folder: str = None, format_string: Union[str, FeatureFormattingType] = None,
                                visible: bool = True, publish: bool = True):
        """Creates a time over time subtraction calculation. For example, create_time_differencing on the feature 'revenue'
        , time level 'date', and a length of 2 will create a feature calculating the revenue today subtracted by the revenue
        two days ago

        Args:
            new_feature_name (str): What the feature will be called.
            numeric_feature_name (str): The numeric feature to use for the calculation.
            time_length (int): The length of the lag in units of the given level of the given time_hierarchy.
            hierarchy_name (str): The time hierarchy used in the calculation.
            level_name (str): The level within the time hierarchy
            description (str): The description for the feature. Defaults to None.
            caption (str): The caption for the feature. Defaults to None.
            folder (str): The folder to put the feature in. Defaults to None.
            format_string (str): The format string for the feature. Defaults to None.
            visible (bool, optional): Whether the feature should be visible. Defaults to True.
            publish (bool): Whether or not the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        existing_measures = get_dmv_data(model=self, fields=[],
                                        id_field=Measure.name)

        model_utils._check_features(features=[numeric_feature_name],
                    check_list=list(existing_measures.keys()))

        if not (type(time_length) == int) or time_length < 1:
            raise atscale_errors.UserError(
                f'Invalid parameter value \'{time_length}\', Length must be an integer greater than zero')
        if new_feature_name in existing_measures:
            raise atscale_errors.UserError(
                f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')

        hier_dict, level_dict = feature_utils._check_time_hierarchy(data_model=self, hierarchy_name=hierarchy_name,
                                                    level_name=level_name)

        time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]
       
        project_json = self.project._get_dict()
        feature_utils._create_time_differencing_feature_local(project_dict = project_json, 
                             cube_id = self.cube_id, time_dimension= time_dimension, 
                             new_feature_name = new_feature_name, numeric_feature_name = numeric_feature_name, 
                             time_length = time_length, hierarchy_name = hierarchy_name, level_name = level_name, 
                             description = description, caption = caption, folder = folder,
                             format_string = format_string, visible = visible)

        self.project._update_project(
            project_json=project_json, publish=publish)

    def create_percentage_features(self, numeric_feature_name: str, hierarchy_name: str,
                        level_names: List[str] = None, new_feature_names: List[str] = None,
                        description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                        visible: bool = True, publish: bool = True):
        """Creates a set of features calculating the percentage of the given numeric_feature's value compared to each non-leaf 
        (i.e. non-base) level in the hierarchy

        Args:
            numeric_feature_name (str): The numeric feature to use for the calculation
            hierarchy_name (str): The hierarchy to use for comparisons
            level_names (List[str], optional): The subset of levels to make percentages for, if None generates 
                percentages for all non-leaf levels. Defaults to None.  
            new_feature_names (List[str], optional): The names of the new columns, if None generates 
                names. If not None it must be same length and order as level_names. Defaults to None.  
            description (str, optional): The description for the feature. Defaults to None.
            caption (str, optional): The caption for the new features. Defaults to None.
            folder (str, optional): The folder to put the new features in. Defaults to None.
            format_string (str, optional): The format string for the features. Defaults to None.
            visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
        """
        model_utils._perspective_check(self)

        hier_dict, level_dict = feature_utils._check_time_hierarchy(
            data_model=self, hierarchy_name=hierarchy_name)

        dimension_name = hier_dict[hierarchy_name][Hierarchy.dimension.name]
        level_list = list(get_dmv_data(model=self, fields=[Level.name, Level.hierarchy],
                                    filter_by={Level.hierarchy: [hierarchy_name]}).keys())
        measure_list = list(get_dmv_data(
            model=self, id_field=Measure.name).keys())

        model_utils._check_features(features=[numeric_feature_name],
                    check_list=measure_list,  # todo: make this check for draft measures too
                    errmsg=f'Invalid parameter value \'{numeric_feature_name}\' is not a numeric feature in the data model')


        # some error checking on the levels
        if level_names:
            if type(level_names) != list:
                level_names = [level_names]
            missing_levels = [x for x in level_names if x not in level_list]
            if missing_levels:
                raise atscale_errors.UserError(
                    f'Level name{"s" if len(missing_levels) > 1 else ""}: {", ".join(missing_levels)} not found '
                    f'in Hierachy: {hierarchy_name}')
            elif level_list[-1] in level_names:
                raise atscale_errors.UserError(
                    f'Cannot create percentage for leaf node of hierarchy: {level_list[-1]}')
        else:
            level_names = level_list[:-1]

        if (new_feature_names is not None) and (len(new_feature_names) != len(level_names)):
            raise atscale_errors.UserError(
                f'Length of new_feature_names must equal length of level_names')


        if not new_feature_names:
            new_feature_names = [numeric_feature_name + '% of ' + level for level in level_names]
        
        bad_names_list = [name for name in new_feature_names if name in measure_list]
        if len(bad_names_list) > 0:
            bad_names = ', '.join(bad_names_list)
            raise atscale_errors.UserError(
                    f'Invalid name parameter: \'{bad_names}\'. Feature already exists with given name')


        project_dict = self.project._get_dict()

        for lev_index, level in enumerate(level_names):
            name = new_feature_names[lev_index]
            feature_utils._create_percentage_feature_local(project_dict=project_dict, cube_id=self.cube_id, new_feature_name=name,
                                    numeric_feature_name=numeric_feature_name, dimension_name=dimension_name,
                                    hierarchy_name=hierarchy_name, level_name=level, description=description,
                                    caption=caption, folder=folder, format_string=format_string, visible=visible)

        self.project._update_project(
            project_json=project_dict, publish=publish)
    
    def create_period_to_date_features(self, numeric_feature_name: str, hierarchy_name: str,
                            level_names: List[str] = None, new_feature_names: List[str] = None,
                            description: str = None, folder: str = None, 
                            format_string: str = None, visible: bool = True, publish: bool = True) -> str:
        """Creates a period-to-date calculation

        Args:
            numeric_feature_name (str): The numeric feature to use for the calculation
            hierarchy_name (str): The time hierarchy used in the calculation            
            level_names (List[str], optional): The subset of levels to make period to date calcs for, if 
                None generates period to date for all non-leaf levels. Defaults to None.  
            new_feature_names (List[str], optional): The names of the new columns, if None generates 
                names. If not None it must be same length and order as level_names. Defaults to None.  
            description (str, optional): The description for the feature. Defaults to None.
            folder (str, optional): The folder to put the feature in. Defaults to None.
            format_string (str, optional): The format string for the feature. Defaults to None.
            visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
            publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

        Returns:
            str: A message containing the names of successfully created features
        """
        model_utils._perspective_check(self)

        hier_dict, level_dictAlt = feature_utils._check_time_hierarchy(
            data_model=self, hierarchy_name=hierarchy_name)
        time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]

        level_list = list(get_dmv_data(model=self, fields=[Level.name, Level.hierarchy],
                                    filter_by={Level.hierarchy: [hierarchy_name]}).keys())
        measure_list = list(get_dmv_data(
            model=self, id_field=Measure.name).keys())

        model_utils._check_features(features=[numeric_feature_name],
                    check_list=measure_list,  # todo: make this check for draft measures too
                    errmsg=f'Invalid parameter value: \'{numeric_feature_name}\' is not a numeric feature in the data model')

        # some error checking on the levels
        if level_names:
            if type(level_names) != list:
                level_names = [level_names]
            missing_levels = [x for x in level_names if x not in level_list]
            if missing_levels:
                raise atscale_errors.UserError(
                    f'Level name{"s" if len(missing_levels) > 1 else ""}: {", ".join(missing_levels)} not found '
                    f'in Hierachy: {hierarchy_name}')
            elif level_list[-1] in level_names:
                raise atscale_errors.UserError(
                    f'Cannot create period for leaf node of hierarchy: {level_list[-1]}')
        else:
            level_names = level_list[:-1]

        if (new_feature_names is not None) and (len(new_feature_names) != len(level_names)):
            raise atscale_errors.UserError(
                f'Length of new_feature_names must equal length of level_names')

        base_level = level_list[-1]
        if not new_feature_names:
            new_feature_names = [numeric_feature_name + '_' + level +'_To_'+ 
                        base_level for level in level_names]
        
        bad_names_list = [name for name in new_feature_names if name in measure_list]
        if len(bad_names_list) > 0:
            bad_names = ', '.join(bad_names_list)
            raise atscale_errors.UserError(
                    f'Invalid name parameter: \'{bad_names}\'. Feature already exists with given name')

        project_json = self.project._get_dict()
        for lev_index, level in enumerate(level_names):
            name = new_feature_names[lev_index]
            feature_utils._create_period_to_date_feature_local(project_dict= project_json, cube_id= self.cube_id, new_feature_name= name,
                                numeric_feature_name= numeric_feature_name, hierarchy_name= hierarchy_name, level_name= level, 
                                base_name = base_level, time_dimension= time_dimension, description= description, folder= folder, 
                                format_string= format_string, visible= visible)

        self.project._update_project(
            project_json=project_json, publish=publish)

    def get_hierarchies(self, secondary_attribute: bool = None, folder_list: List[str] = None) -> Dict:
        """Gets a dictionary of dictionaries with the hierarchies names and metadata. Secondary attributes are treated as
             their own hierarchies so they are included by default, but can be filtered with the secondary_attribute parameter.

        Args: 
            secondary_attribute (bool, optional): if we want to filter the secondary attribute field. True will return only
                secondary_attributes, False will return non-seconary attributes, None will return all Hierarchies. Defaults to None.
            folder_list (List[str], optional): The list of folders in the data model containing hierarchies to exclusively list.
                Defaults to None to not filter by folder.

        Returns:
            dict: A dictionary of dictionaries where the hierarchy names are the keys in the outer dictionary
                while the inner keys are the following: 'dimension', 'description', 'caption', 'folder', 'type'(value is 
                Time or Standard), 'secondary_attribute'.
        """
        filter_by = {}
        if secondary_attribute is not None:
            filter_by[Hierarchy.secondary_attribute] = [secondary_attribute]

        #folder list is more involved as we need to append if the dict already exists
        if folder_list is not None:
            if type(folder_list) == str: 
                folder_list = [folder_list]
            filter_by[Hierarchy.folder] = folder_list

        return metadata_utils._get_hierarchies(self, filter_by= filter_by)

    def get_hierarchy_levels(self, hierarchy_name: str) -> List[str]:
        """Gets a list of strings for the levels of a given hierarchy

        Args:
            hierarchy_name (str): The name of the hierarchy

        Returns:
            List[str]: A list containing the hierarchy's levels
        """
        return metadata_utils._get_hierarchy_levels(self, hierarchy_name)

    def get_feature_description(self, feature: str) -> str:
        """Returns the description of a given feature.

        Args:
            feature (str): The query name of the feature to retrieve the description of.

        Returns:
            str: The description of the given feature.
        """
        return metadata_utils._get_feature_description(self, feature)

    def get_feature_expression(self, feature: str) -> str:
        """Returns the expression of a given feature.

        Args:
            feature (str): The query name of the feature to return the expression of.

        Returns:
            str: The expression of the given feature.
        """
        return metadata_utils._get_feature_expression(self, feature=feature)

    def get_all_numeric_feature_names(self, folder: str = None) -> List[str]:
        """Returns a list of all numeric features (ie Aggregate and Calculated Measures) in the data model.

        Args:
            folder (str, optional): The name of a folder in the data model containing measures to exclusively list.
                Defaults to None to not filter by folder.

        Returns:
            List[str]: A list of the query names of numeric features in the data model and, if given, in the folder.
        """
        return metadata_utils._get_all_numeric_feature_names(self, folder= folder)

    def get_all_categorical_feature_names(self, folder: str = None) -> List[str]:
        """Returns a list of all categorical features (ie Hierarchy levels and secondary_attributes) in the given DataModel.

        Args:
            folder (str, optional): The name of a folder in the DataModel containing features to exclusively list.
                Defaults to None to not filter by folder.
        
        Returns:
            List[str]: A list of the query names of categorical features in the DataModel and, if given, in the folder.
        """
        return metadata_utils._get_all_categorical_feature_names(self, folder= folder)

    def get_folders(self) -> List[str]:
        """Returns a list of the available folders in the given DataModel.
        
        Returns:
            List[str]: A list of the available folders
        """
        return metadata_utils._get_folders(self)

    def get_connected_warehouse(self):
        """Returns the warehouse id utilized in this data_model

        Returns:
            str: the warehouse id 
        """
        return self.project.get_connected_warehouse()

    def list_related_hierarchies(self, dataset_name: str) -> List[str]:
        """Returns a list of all hierarchies with relationships to the given dataset.

        Args:
            dataset_name (str): The name of a fact dataset to find relationships from.
        
        Returns:
            List[str]: A list of the names of the hierarchies that have relationships to the dataset.
        """
        project_dict = self.project._get_dict()
        cube_dict = model_utils._get_model_dict(self, project_dict= project_dict)[0]
        # first find the dataset from the input name
        dataset = dictionary_parser.parse_dict_list(project_parser.get_datasets(project_dict), 'name', dataset_name)
        if dataset is None:
            raise atscale_errors.UserError(f'No fact dataset named "{dataset_name}" found')
        # find the dataset reference using the id
        key_ref_ids = []
        dataset_ref = dictionary_parser.parse_dict_list(data_model_parser._get_cube_datasets(cube_dict), 'id', dataset.get('id'))
        if dataset_ref is None:
            raise atscale_errors.UserError(f'No fact dataset named "{dataset_name}" found')
        # grab all key-refs from the dataset so we can find the attributes
        for key_ref in dataset_ref.get('logical', {}).get('key-ref', []):
            key_ref_ids.append(key_ref.get('id'))
        # loop through project and cube attributes to find matches
        keyed_attribute_ids = []
        for keyed_attribute in project_dict.get('attributes', {}).get('keyed-attribute') + cube_dict.get('attributes', {}).get('keyed-attribute'):
            if keyed_attribute.get('key-ref') in key_ref_ids:
                keyed_attribute_ids.append(keyed_attribute.get('id'))
        # loop through project and cube hierarchies to grab the ones that contain the matched attributes
        hierarchy_names = set()
        for dimension in project_dict.get('dimensions', {}).get('dimension', []) + cube_dict.get('dimensions', {}).get('dimension', []):
            for hierarchy in dimension.get('hierarchy', []):
                for level in hierarchy.get('level', []):
                    if level.get('primary-attribute') in keyed_attribute_ids:
                        hierarchy_names.add(hierarchy.get('name'))
                        break
        # augment the list with any other hierarchies that are connected to them with snowflake dimensions
        hierarchy_names = list(hierarchy_names)
        model_utils._add_related_hierarchies(self, hierarchy_names)
        return hierarchy_names

    def list_related_datasets(self, hierarchy_name: str) -> List[str]:
        """Returns a list of all fact datasets with relationships to the given hierarchy.

        Args:
            hierarchy_name (str): The name of a hierarchy to find relationships from.
        
        Returns:
            List[str]: A list of the names of the datasets that have relationships to the hierarchy.
        """
        project_dict = self.project._get_dict()
        cube_dict = model_utils._get_model_dict(self, project_dict= project_dict)[0]
        # make sure we got a valid hierarchy
        keyed_attribute_ids = []
        for dimension in project_dict.get('dimensions', {}).get('dimension', []) + cube_dict.get('dimensions', {}).get('dimension', []):
            hierarchy = dictionary_parser.parse_dict_list(dimension.get('hierarchy', []), 'name', hierarchy_name)
            if hierarchy is not None:
                break
        if hierarchy is None:
            raise atscale_errors.UserError(f'No hierarchy named "{hierarchy_name}" found')
        # the hierarchy we were passed could be a part of a snowflake dimension so we need to add related ones 
        hierarchy_names = [hierarchy.get('name')]
        model_utils._add_related_hierarchies(self, hierarchy_names)
        # loop through project and cube hierarchies and grab their attributes if they were in the list
        for dimension in project_dict.get('dimensions', {}).get('dimension', []) + cube_dict.get('dimensions', {}).get('dimension', []):
            for hierarchy in dimension.get('hierarchy', []):
                if hierarchy.get('name') in hierarchy_names:
                    for level in hierarchy.get('level', []):
                        keyed_attribute_ids.append(level.get('primary-attribute'))

        # loop through project and cube attributes to find matches
        key_ref_ids = []
        for keyed_attribute in project_dict.get('attributes', {}).get('keyed-attribute') + cube_dict.get('attributes', {}).get('keyed-attribute'):
            if keyed_attribute.get('id') in keyed_attribute_ids:
                key_ref_ids.append(keyed_attribute.get('key-ref'))
        # find the dataset refs that contain the matched attributes
        dataset_ids = set()
        for dataset_ref in data_model_parser._get_cube_datasets(cube_dict):
            for key_ref in dataset_ref.get('logical', {}).get('key-ref', []):
                if key_ref.get('id') in key_ref_ids:
                    dataset_ids.add(dataset_ref.get('id'))
                    break
        # find the datasets that the refs match to so we can grab the names
        dataset_names = []
        for dataset in project_parser.get_datasets(project_dict):
            if dataset.get('id') in dataset_ids:
                dataset_names.append(dataset.get('name'))
        return dataset_names
