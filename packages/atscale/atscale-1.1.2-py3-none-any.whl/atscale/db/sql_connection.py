from abc import ABC, abstractmethod

from pandas import DataFrame, read_sql_query
from atscale.parsers import project_parser

from atscale.utils.enums import PlatformType, TableExistsActionType


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

    def dispose_engine(self):
        """
        Use this method to close the engine and any associated connections in its connection pool. 

        If the user changes the connection parameters on an sql_connection object then  dispose() should be called so any current
        connections (and engine) is cleared of all state before establishing a new connection (and engine and connection pool). Probably
        don't want to call this in other situations. From the documentation: https://docs.sqlalchemy.org/en/13/core/connections.html#engine-disposal

        <The Engine is intended to normally be a permanent fixture established up-front and maintained throughout the lifespan of an application. 
        It is not intended to be created and disposed on a per-connection basis>
        """
        if hasattr(self, '_engine') and self._engine is not None:
            self._engine.dispose()
            # setting none will cause the getter for engine to grab the connection
            # URL anew and create the engine rather than hanging onto a diposed one
            self._engine = None

    @abstractmethod
    def _get_connection_url(self) -> str:
        """Constructs a connection url from the instance variables needed to interact with the DB

        Returns:
            str: The connection url to the DB of interest
        """
        raise NotImplementedError

    def execute_statements(self, statements: list):
        """Executes a list of SQL statements. Does not return any results but may trigger an exception. 

        Args:
            statements (list): a list of SQL statements to execute.
        """
        from sqlalchemy import text
        with self.engine.connect() as connection:
            for statement in statements:
                connection.execute(text(statement))

    def submit_queries(self, query_list: list) -> list:
        """Submits a list of queries, collecting the results in a list of dictionaries. 

        Args:
            query_list (list): a list of queries to submit. 

        Returns:
            list(DataFrame): A list of pandas DataFrames containing the results of the queries.
        """
        results = []
        # This uses "with" for transaction management on the connection. If this is unfamiliar,
        # please see: https://docs.sqlalchemy.org/en/14/core/connections.html#using-transactions
        with self.engine.connect() as connection:
            for query in query_list:
                # read_sql_query is a pandas function,  but takes an SQLAlchemy connection object (or a couple other types).
                # https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html
                # see test_snowflake.test_quoted_columns for discussion related to any potential changes to using read_sql_query
                results.append(read_sql_query(query, connection))
        return results

    def submit_query(self, query: str) -> DataFrame:
        """This submits a single query and reads the results into a DataFrame. It closes the connection after each query. 
        If you will be executing more than one statement or conducting more involved interactions with the database, you 
        can get get the connection string directly and perform your own connection management. 

        Args:
            query (str): SQL statement to be executed

        Returns:
            DataFrame: the results of executing the SQL statement or query parameter, read into a DataFrame
        """
        return self.submit_queries([query])[0]

    def _fix_table_name(self, table_name: str):
        return table_name

    def _fix_column_name(self, column_name: str):
        return column_name

    @abstractmethod
    def write_df_to_db(self, table_name: str, dataframe: DataFrame, if_exists: TableExistsActionType = TableExistsActionType.FAIL):
        """Writes the provided pandas DataFrame into the provided table name. Can pass in the intended behavior in case
            the provided table name is already taken.

        Args:
            table_name (str): What table to write the dataframe into
            dataframe (DataFrame): The pandas DataFrame to write into the table
            if_exists (TableExistsActionType, optional): The intended behavior in case of table name collisions. 
                Defaults to TableExistsActionType.FAIL.
        """
        raise NotImplementedError

    def _verify_connection(self, project_datasets, connections):
        """Compares connection information for a project with the information related to this connection. 
        """
        datasets = []
        cons = []
        connections = project_parser.get_connection_list_for_project_datasets(
            project_datasets, connections)
        for i in range(0,  len(connections)):
            if self._verify(project_datasets[i], connections[i]):
                datasets.append(project_datasets[i])
                cons.append(connections[i])
        return [datasets, cons]

    def _verify(self, mod: dict, con: dict) -> bool:
        if con is None:
            return False

        if con.get('platformType') != self.platform_type.value:
            return False
        
        return True


