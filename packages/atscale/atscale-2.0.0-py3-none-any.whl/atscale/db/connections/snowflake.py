import getpass
import inspect
from typing import Dict
import cryptocode
import pandas as pd

from atscale.errors.atscale_errors import AtScaleExtrasDependencyImportError, UserError
from atscale.db.sqlalchemy_connection import SQLAlchemyConnection
from atscale.base.enums import PlatformType, PysparkTableExistsActionType, PandasTableExistsActionType


class Snowflake(SQLAlchemyConnection):
    """The child class of SQLConnection whose implementation is meant to handle 
        interactions with a Snowflake DB. 
    """

    platform_type: PlatformType = PlatformType.SNOWFLAKE

    def __init__(self, username: str, account: str, warehouse: str,
                 database: str, schema: str, password: str = None, role: str = None):
        """Constructs an instance of the Snowflake SQLConnection. Takes arguments necessary to find the warehouse, database, 
            and schema. If password is not provided, it will prompt the user to login.

        Args:
            username (str): the username necessary for login
            account (str): the account of the intended Snowflake connection            
            warehouse (str): the warehouse of the intended Snowflake connection
            database (str): the database of the intended Snowflake connection
            schema (str): the schema of the intended Snowflake connection
            password (str, optional): the password associated with the username. Defaults to None.
            role (str, optional): the role associated with the username. Defaults to None.
        """
        super().__init__()

        try:
            from sqlalchemy import create_engine
            from snowflake.connector.pandas_tools import pd_writer
        except ImportError as e:
            raise AtScaleExtrasDependencyImportError('snowflake', str(e))

        localVars = locals()
        inspection = inspect.getfullargspec(self.__init__)
        # list of all parameters names in order (optionals must come after required)
        all_params = inspection[0]
        # tuple of default values (for every optional parameter)
        defaults = inspection[3]
        # parameter has default if and only if its optional
        param_name_list = all_params[:-len(defaults)]
        param_names_none = [x for x in param_name_list if localVars[x] is None]

        if param_names_none:
            raise ValueError(
                f'The following required parameters are None: {", ".join(param_names_none)}')

        self._username = username
        self._account = account
        self._warehouse = warehouse
        self._database = database
        self._schema = schema
        if password:
            self._password = cryptocode.encrypt(
                password, self.platform_type.value)
        else:
            self._password = None
        self._role = role

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        self.dispose_engine()

    @property
    def account(self) -> str:
        return self._account

    @account.setter
    def account(self, value):
        self._account = value
        self.dispose_engine()

    @property
    def warehouse(self) -> str:
        return self._warehouse

    @warehouse.setter
    def warehouse(self, value):
        self._warehouse = value
        self.dispose_engine()

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, value):
        self._database = value
        self.dispose_engine()

    @property
    def schema(self) -> str:
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value
        self.dispose_engine()

    @property
    def password(self) -> str:
        raise Exception(
            "Passwords cannot be retrieved.")

    @password.setter
    def password(self, value):
        self._password = cryptocode.encrypt(value, self.platform_type.value)
        self.dispose_engine()

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value):
        self._role = value
        self.dispose_engine()

    def _get_connection_url(self):
        if not self._password:
            self._password = cryptocode.encrypt(getpass.getpass(
                prompt='Please enter your password for Snowflake: '), self.platform_type.value)
        password = cryptocode.decrypt(self._password, self.platform_type.value)
        connection_url = f'snowflake://{self._username}:{password}@{self._account}/{self._database}/{self._schema}?warehouse={self._warehouse}'
        if self._role:
            connection_url += f'&role={self._role}'
        return connection_url

    def _fix_table_name(self, table_name: str):
        """Required for snowflake, which requires lowercase for writing to a database when method is "replace" if the table exists.

        Args:
            table_name (str): the table name

        Returns:
            str: the table name, potentially changed to upper, lower, or mixed case as required by the implementing database
        """
        return table_name.lower()

    def _fix_column_name(self, column_name: str) -> str:
        """Required for snowflake, which requires uppercase column names when writing a dataframe to a table. 

        Args:
            column_name (str): the column name

        Returns:
            str: the column name, potentially changed to upper, lower, or mixed case as required by the implementing database
        """
        return column_name.upper()

    def write_df_to_db(self, table_name, dataframe: pd.DataFrame, if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL, chunksize=10000):
        from snowflake.connector.pandas_tools import pd_writer
        fixed_df = dataframe.rename(columns=lambda c: self._fix_column_name(c))
        fixed_table_name = self._fix_table_name(table_name)
        fixed_df.to_sql(name=fixed_table_name, con=self.engine, schema=self._schema, if_exists=if_exists.value, index=False,
                        chunksize=chunksize, method=pd_writer)

    def write_pysparkdf_to_db(self, pyspark_dataframe, jdbc_format: str, jdbc_options: Dict[str, str],
                             table_name: str = None, if_exists: PysparkTableExistsActionType =
                             PysparkTableExistsActionType.ERROR):
                             
        from functools import reduce 
        try:
            from pyspark.sql import SparkSession  
        except ImportError as e:
            raise AtScaleExtrasDependencyImportError('jdbc', str(e))

        columnsToSwitch = pyspark_dataframe.columns
        newColumnNames = [self._fix_column_name(x) for x in columnsToSwitch]
        
        pyspark_dataframe_renamed = reduce(lambda data, idx: 
        data.withColumnRenamed(columnsToSwitch[idx], newColumnNames[idx]), range(len(columnsToSwitch)), pyspark_dataframe)


        if table_name is not None:
            fixed_table_name = self._fix_table_name(table_name)
        else: 
            fixed_table_name = None

        if jdbc_options.get('dbtable') is not None:
            jdbc_options['dbtable'] = self._fix_table_name(jdbc_options['dbtable'])
        
        super().write_pysparkdf_to_db(pyspark_dataframe_renamed, jdbc_format, jdbc_options, fixed_table_name,if_exists)

    # def verify(self, project_dataset: dict, connection: dict) -> bool:
        # check the connection information
    #    if connection is None:
    #        return False

    #    if connection.get('platformType') != self.platform_type.value:
    #        return False

        # We cannot use the database value on a connection from the org to verify. This is because the project json
        # can refer to a database that is different from the original one used when setting up the connection for the org.
        # So at this point,  unless we figure out how to check port or host (snowflake does host in a weird way), I don't
        # think we can use any other info from the actual connection info to verify. The rest of the info we have to use from
        # the project, which I do below.

        # check info in the project_dataset which points at the connection (so database should agree)
    #    if project_dataset is None:
    #        return False

    #    phys = project_dataset.get('physical')
    #    if phys is None:
    #        return False

    #    tables = phys.get('tables')
    #    if tables is None:
    #        return False

        # Apparently tables is a list so there can be more than one?
        # Not sure what that means for verification. We'll look for at least one that matches.
    #    for table in tables:
    #        if table.get('database') == self._database and table.get('schema') == self._schema:
    #            return True

    #    return False
