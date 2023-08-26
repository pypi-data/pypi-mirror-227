import getpass
import cryptocode
import inspect
import logging

from pandas import DataFrame, read_sql_query

from atscale.errors.atscale_errors import AtScaleExtrasDependencyImportError
from atscale.db.sql_connection import SQLConnection
from atscale.base.enums import PlatformType, PandasTableExistsActionType

logger = logging.getLogger(__name__)

class Synapse(SQLConnection):
    """The child class of SQLConnection whose implementation is meant to handle 
        interactions with a Synapse DB. 
    """
    platform_type: PlatformType = PlatformType.SYNAPSE

    conversion_dict = {
        '<class \'numpy.int64\'>': 'int',
        '<class \'numpy.float64\'>': 'real',
        '<class \'str\'>': 'nvarchar(4000)',
        '<class \'numpy.bool_\'>': 'bit',
        '<class \'pandas._libs.tslibs.timestamps.Timestamp\'>': 'datetime',
        '<class \'datetime.date\'>': 'date',
        }

    def __init__(self, username:str, host:str, database:str, driver:str, schema:str, port:int=1433, password:str=None):
        """Constructs an instance of the Synapse SQLConnection. Takes arguments necessary to find the database, driver,
            and schema. If password is not provided, it will prompt the user to login.

        Args:
            username (str): the username necessary for login
            host (str): the host of the intended Synapse connection
            database (str): the database of the intended Synapse connection
            driver (str): the driver of the intended Synapse connection
            schema (str): the schema of the intended Synapse connection
            port (int, optional): A port if non-default is configured. Defaults to 1433.
            password (str, optional): the password associated with the username. Defaults to None.
        """
        try:
            import pyodbc as po
        except ImportError as e:
            raise AtScaleExtrasDependencyImportError('synapse', str(e))

        localVars = locals()
        inspection = inspect.getfullargspec(self.__init__)
        all_params = inspection[0]  # list of all parameters names in order (optionals must come after required)
        defaults = inspection[3]  # tuple of default values (for every optional parameter)
        param_name_list = all_params[:-len(defaults)]  # parameter has default if and only if its optional
        param_names_none = [x for x in param_name_list if localVars[x] is None]

        if param_names_none:
            raise ValueError(
                f'The following required parameters are None: {", ".join(param_names_none)}')

        self.username = username
        self.host = host
        self.database = database
        self.driver = driver
        self.schema = schema
        self.port = port
        if password:
            self._password = cryptocode.encrypt(password,self.platform_type.value)
        else:
            self._password = None

        try:
            validation_connection = po.connect(self._get_connection_url(), autommit=True)
            validation_connection.close()
        except:
            logger.error('Unable to create database connection, please verify the inputs')
            raise


    @property
    def password(self) -> str:
        raise Exception(
           "Passwords cannot be retrieved.")

    @password.setter
    def password(self, value):
        self._password = cryptocode.encrypt(value,self.platform_type.value)

    def _get_connection_url(self):
        if not self._password:
            self._password = cryptocode.encrypt(getpass.getpass(prompt='Please enter your Synapse password: '),self.platform_type.value)
        password = cryptocode.decrypt(self._password,self.platform_type.value)
        connection_url = f'DRIVER={self.driver};SERVER={self.host};PORT={self.port};DATABASE={self.database};UID={self.username};PWD={password}'
        return connection_url

    def _format_types(self, dataframe: DataFrame) -> dict:
        types = {}
        for i in dataframe.columns:
            if str(type(dataframe[i].loc[~dataframe[i].isnull()].iloc[0])) in self.conversion_dict:
                types[i] = self.conversion_dict[str(
                    type(dataframe[i].loc[~dataframe[i].isnull()].iloc[0]))]
            else:
                types[i] = self.conversion_dict['<class \'str\'>']
        return types

    def _create_table(self, table_name: str, types: dict, cursor):
        # TODO: other than customization of the formatting, I think this is the same as what is in iris,
        # so could try and abstract this out into a superclass, but right now there's only 2 of them so
        # not worth the effort.
        if not cursor.tables(table=table_name, tableType='TABLE').fetchone():
            operation = f"CREATE TABLE \"{self.schema}\".\"{table_name}\" ("
            for key, value in types.items():
                operation += f"{key} {value}, "
            operation = operation[:-2]
            operation += ")"
            cursor.execute(operation)
        return types

    def write_df_to_db(self, table_name: str, dataframe: DataFrame, if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL, chunksize: int = 10000):
        # similar to create table, I think thisis the same as iris, though it's using different
        # python formatting commands, though I think to the same effect (though with a different dict).
        # TODO: could extract this out into a super class, but since only two classes do this, not yet worth the effort
        import pyodbc
        connection = pyodbc.connect(self._get_connection_url(), autommit=True)
        cursor = connection.cursor()

        if cursor.tables(table=table_name, schema=self.schema).fetchone():
            exists = True
        else:
            exists = False

        if exists and if_exists == PandasTableExistsActionType.FAIL:
            raise Exception(
                f'A table named: {table_name} already exists in schema: {self.schema}')

        types = self._format_types(dataframe)

        if exists and if_exists == PandasTableExistsActionType.REPLACE:  # if replace, then drop and recreate the table
            operation = f"DROP TABLE \"{self.schema}\".\"{table_name}\""
            cursor.execute(operation)
            self._create_table(table_name, types, cursor)
        elif not exists:
            self._create_table(table_name, types, cursor)

        operation = f"INSERT INTO \"{self.schema}\".\"{table_name}\" ("
        for col in dataframe.columns:
            operation += f"{col}, "
        operation = operation[:-2]
        operation += ") "

        list_df = [dataframe[i:i + chunksize]
                   for i in range(0, dataframe.shape[0], chunksize)]
        for df in list_df:
            op_copy = operation
            for index, row in df.iterrows():
                op_copy += 'SELECT '
                for cl in df.columns:
                    if 'nvarchar' in types[cl] or 'date' in types[cl]:
                        op_copy += "'{}', ".format(row[cl])
                    else:
                        op_copy += "{}, ".format(row[cl])
                op_copy = op_copy[:-2]
                op_copy += " UNION ALL "
            op_copy = op_copy[:-11]
            cursor.execute(op_copy)
        cursor.close()
        connection.close()

    def execute_statements(self, statements: list):
        #same implementation is in IRIS, so if you need to change one please change the other
        import pyodbc as po
        with po.connect(self.connection_string, autocommit=False) as connection:
            with connection.cursor() as cursor: 
                for statement in statements:
                    cursor.execute(statement)
                    connection.commit()

    def submit_query(self, query):
        import pyodbc as po
        with po.connect(self.connection_string, autocommit=True) as connection:
            df = read_sql_query(query, connection)
        return df

    def submit_queries(self, query_list: list) -> list:
        import pyodbc as po
        results = []
        with po.connect(self.connection_string, autocommit=True) as connection:
            for query in query_list:
                results.append(read_sql_query(query, connection))
        return results
