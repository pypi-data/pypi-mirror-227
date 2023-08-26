from abc import ABC, abstractmethod
from typing import Dict

from pandas import DataFrame

from atscale.base.enums import PlatformType, PandasTableExistsActionType, PysparkTableExistsActionType
from atscale.errors import atscale_errors
from copy import deepcopy

class SQLConnection(ABC):
    """The abstract class meant to standardize functionality related to various DB systems that AI-Link supports.
        This includes submitting queries, writeback, and engine disposal.
    """

    platform_type: PlatformType
    """The enum representing platform type. Used in validating connections between AtScale DataModels and their 
        source databases"""

    @property
    def platform_type(self) -> PlatformType:
        """Getter for the instance type of this SQLConnection

        Returns:
            PlatformType: Member of the PlatformType enum
        """
        return SQLConnection.platform_type

    @platform_type.setter
    def platform_type(self, value):
        """Setter for the platform_type instance variable. This variable is final, please construct a new SQLConnection.

        Args:
            value: setter cannot be used.

        Raises:
            Exception: Raises a value if the setter is attempted.
        """
        raise Exception(
            "It is not possible to change the platform type of a SQLConnection class. Please create an instance of the desired platform type.")


    @abstractmethod
    def submit_query(self, query: str) -> DataFrame:
        """This submits a single query and reads the results into a DataFrame. It closes the connection after each query. 

        Args:
            query (str): SQL statement to be executed

        Returns:
            DataFrame: the results of executing the SQL statement or query parameter, read into a DataFrame
        """
        raise NotImplementedError

    @abstractmethod
    def submit_queries(self, query_list: list) -> list:
        """Submits a list of queries, collecting the results in a list of dictionaries. 

        Args:
            query_list (list): a list of queries to submit. 

        Returns:
            list(DataFrame): A list of pandas DataFrames containing the results of the queries.
        """
        raise NotImplementedError

    @abstractmethod
    def execute_statements(self, statements: list):
        """Executes a list of SQL statements. Does not return any results but may trigger an exception. 

        Args:
            statements (list): a list of SQL statements to execute.
        """
        raise NotImplementedError

    def _fix_table_name(self, table_name: str):
        return table_name

    def _fix_column_name(self, column_name: str):
        return column_name

    @abstractmethod
    def write_df_to_db(self, table_name: str, dataframe: DataFrame, dtypes:dict = None, if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL, chunksize: int = 1000):
        """Writes the provided pandas DataFrame into the provided table name. Can pass in if_exists to indicate the intended behavior if
            the provided table name is already taken.

        Args:
            table_name (str): What table to write the dataframe into
            dataframe (DataFrame): The pandas DataFrame to write into the table
            dtypes (dict, optional): the datatypes of the passed dataframe. Keys should match the column names. Defaults to None
                and type will be text. 
            if_exists (PandasTableExistsActionType, optional): The intended behavior in case of table name collisions. 
                Defaults to PandasTableExistsActionType.FAIL.
            chunksize (int, optional): the chunksize for the write operation.
        """
        raise NotImplementedError

    def write_pysparkdf_to_external_db(self, pyspark_dataframe, jdbc_format: str, jdbc_options: Dict[str, str],
                             table_name: str = None, if_exists: PysparkTableExistsActionType =
                              PysparkTableExistsActionType.ERROR):
        """Writes the provided pyspark DataFrame into the provided table name via jdbc. Can pass in if_exists to indicate the intended behavior if
            the provided table name is already taken.

        Args:
            pyspark_dataframe (pyspark.sql.DataFrame): The pyspark dataframe to write
            jdbc_format (str): the driver class name. For example: 'jdbc', 'net.snowflake.spark.snowflake', 'com.databricks.spark.redshift' 
            jdbc_options (Dict[str,str]): Case-insensitive to specify connection options for jdbc 
            table_name (str): What table to write the dataframe into, can be none if 'dbtable' option specified
            if_exists (PysparkTableExistsActionType, optional): The intended behavior in case of table name collisions. 
                Defaults to PysparkTableExistsActionType.ERROR.
        """
        try:
            from pyspark.sql import SparkSession 
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError('spark', str(e))

        #we want to avoid editing the source dictionary
        jdbc_copy = deepcopy(jdbc_options)

        #quick check on passed tablename parameters
        if jdbc_copy.get('dbtable') is None:
            if table_name is None:
                raise atscale_errors.UserError('A table name must be specified for the written table. This can be done '\
                    'either through the jdbc_options key "dbtable" or the table_name function parameter')
            else:
                jdbc_copy['dbtable'] = table_name
        elif table_name is not None:
            if table_name != jdbc_copy.get('dbtable'):
                raise atscale_errors.UserError('Different table names passed via the jdbc_options key "dbtable" '\
                     'and the table_name function parameter. Please get one of the 2 options')

        pyspark_dataframe.write.format(jdbc_format).options(**jdbc_copy) \
                        .mode(if_exists.value).save()


    def write_pysparkdf_to_spark_db(self, pyspark_dataframe, table_name: str,
                              alt_database_path: str = None,
                              if_exists: PysparkTableExistsActionType = PysparkTableExistsActionType.ERROR):
        """Writes the provided pyspark DataFrame into the provided table name via standard spark sql operation. Can pass in if_exists to indicate the intended behavior if
            the provided table name is already taken.

        Args:
            pyspark_dataframe (pyspark.sql.DataFrame): The pyspark dataframe to write
            table_name (str): What table to write the dataframe into, will write to default database if none specified
            alt_database_path (str, optional): The alternate database path to use. Will be added as a prefix to the tablename. 
                Defaults to None, and uses the default database if None. Include the trailing delimiter to go between path and tablename.
            if_exists (PysparkTableExistsActionType, optional): The intended behavior in case of table name collisions. 
                Defaults to PysparkTableExistsActionType.ERROR.
        """
        try:
            from pyspark.sql import SparkSession 
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError('spark', str(e))

        if alt_database_path is not None:
            table_name = alt_database_path + table_name
        pyspark_dataframe.write.saveAsTable(table_name).mode(if_exists.value)

    def _verify(self, con: dict) -> bool:
        if con is None:
            return False

        if self.platform_type.value not in con.get('platformType'):
            return False

        return True
