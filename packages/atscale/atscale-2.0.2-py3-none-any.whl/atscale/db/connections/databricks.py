from pandas import DataFrame
import cryptocode
import getpass
import inspect

from atscale.errors.atscale_errors import AtScaleExtrasDependencyImportError
from atscale.db.sql_connection import SQLConnection
from atscale.db.sqlalchemy_connection import SQLAlchemyConnection
from atscale.base.enums import PlatformType, PandasTableExistsActionType

class Databricks(SQLAlchemyConnection):
    """The child class of SQLConnection whose implementation is meant to handle 
        interactions with Databricks. 
    """
    platform_type: PlatformType = PlatformType.DATABRICKS

    conversion_dict = {
    '<class \'numpy.int32\'>': 'INT',
    '<class \'numpy.int64\'>': 'BIGINT',
    '<class \'numpy.float64\'>': 'DOUBLE',
    '<class \'str\'>': 'STRING',
    '<class \'numpy.bool_\'>': 'BOOLEAN',
    '<class \'pandas._libs.tslibs.timestamps.Timestamp\'>': 'TIMESTAMP',
    '<class \'datetime.date\'>': 'DATE',
    '<class \'decimal.Decimal\'>': 'DECIMAL'
    }

    def __init__(self, host:str, schema:str, http_path:str, token:str = None, port:int = 443):
        """Constructs an instance of the Databricks SQLConnection. Takes arguments necessary to find the host 
            and schema. Since prompting login is not viable, this requires an authorization token.

        Args:
            token (str): The authorization token needed to interact with Databricks.
            host (str): The host of the intented Databricks connections
            schema (str): The schema of the intented Databricks connections
            http_path (str): The web path of the intented Databricks connections
            port (int, optional): A port for the connection. Defaults to 443.
        """
        super().__init__()

        try:
            from sqlalchemy import create_engine
            from databricks import sql
        except ImportError as e:
            raise AtScaleExtrasDependencyImportError('databricks', str(e))


        localVars = locals()
        inspection = inspect.getfullargspec(self.__init__)
        all_params = inspection[0]  # list of all parameters names in order (optionals must come after required)
        defaults = inspection[3]  # tuple of default values (for every optional parameter)
        param_name_list = all_params[:-len(defaults)]  # parameter has default if and only if its optional
        param_names_none = [x for x in param_name_list if localVars[x] is None]
        
        if param_names_none:
            raise ValueError(
                f'The following required parameters are None: {", ".join(param_names_none)}')

        if token:
            self._token = cryptocode.encrypt(token,self.platform_type.value)
        else:
            self._token = None
        self._host = host
        self._schema = schema
        self._http_path = http_path
        self._port = port

    @property
    def token(self) -> str:
        raise Exception(
           "Token cannot be retrieved.")

    @token.setter
    def token(self, value):
        self._token = cryptocode.encrypt(value,self.platform_type.value)
        self.dispose_engine()

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value):
        self._host = value
        self.dispose_engine()

    @property
    def schema(self) -> str:
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value
        self.dispose_engine()

    @property
    def http_path(self) -> str:
        return self._http_path

    @http_path.setter
    def http_path(self, value):
        self._http_path = value
        self.dispose_engine()

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value):
        self._port = value
        self.dispose_engine()

    @property
    def engine(self):
        if self._engine is not None:
            return self._engine
        from sqlalchemy import create_engine
        url = self._get_connection_url()
        parameters = self._get_connection_parameters()
        self._engine = create_engine(url, parameters)
        return self._engine

    def _get_connection_url(self):
        from sqlalchemy.engine import URL

        if not self._token:
            self._token = cryptocode.encrypt(getpass.getpass(prompt='Please enter your Databricks token: '), self.platform_type.value)
        token = cryptocode.decrypt(self._token, self.platform_type.value)
        connection_url = URL.create('databricks+connector', username='token',
                                    password=token, host=self._host, port=self._port,
                                    database=self._schema)
        return connection_url

    def _get_connection_parameters(self):
        parameters = {
            'http_path': self._http_path}
        return parameters


    #def write_df_to_db(self, table_name: str, dataframe: DataFrame, if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL, chunksize: int = 1000):
    #    with self.engine.connect() as connection:
    #        dataframe.to_sql(name=table_name, con=connection, schema=self._schema, method='multi', index=False,
    #                         chunksize=chunksize, if_exists=if_exists.value)

    def _format_types(self, dataframe: DataFrame) -> dict:
        types = {}
        for i in dataframe.columns:
            if str(type(dataframe[i].loc[~dataframe[i].isnull()].iloc[0])) in Databricks.conversion_dict:
                types[i] = self.conversion_dict[str(
                    type(dataframe[i].loc[~dataframe[i].isnull()].iloc[0]))]
            else:
                types[i] = self.conversion_dict['<class \'str\'>']
        return types

    def _create_table(self, table_name: str, types: dict, cursor):
        # If the table exists we'll just let this fail and raise the appropriate exception.
        # Related checking to handle gracefully is within calling methods.

        if not cursor.tables(table_name=table_name, table_types=['TABLE']).fetchone():
            operation = "CREATE TABLE `{}`.`{}` (".format(
                self.schema, table_name)
            for key, value in types.items():
                operation += "`{}` {}, ".format(key, value)
            operation = operation[:-2]
            operation += ")"
            cursor.execute(operation)
            # autocommit should be on by default

    def write_df_to_db(self, table_name: str, dataframe: DataFrame, if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL, chunksize: int = 250):
        from databricks import sql

        connection = sql.connect(
        server_hostname=self._host,
        http_path=self._http_path,
        access_token=cryptocode.decrypt(self._token, self.platform_type.value))
        cursor = connection.cursor()

        if cursor.tables(table_name=table_name, schema_name=self.schema).fetchone():
            exists = True
        else:
            exists = False

        if exists and if_exists == PandasTableExistsActionType.FAIL:
            raise Exception(
                f'A table named: {table_name} already exists in schema: {self.schema}')

        types = self._format_types(dataframe)

        if exists and if_exists == PandasTableExistsActionType.REPLACE:
            operation = f"DROP TABLE `{self.schema}`.`{table_name}`"
            cursor.execute(operation)
            self._create_table(table_name, types, cursor)
        elif not exists:
            self._create_table(table_name, types, cursor)

        operation = f"INSERT INTO `{self.schema}`.`{table_name}` VALUES ("

        list_df = [dataframe[i:i + chunksize] for i in range(0, dataframe.shape[0], chunksize)]
        for df in list_df:
            op_copy = operation
            for index, row in df.iterrows():
                for col in df.columns:
                    if 'STRING' in types[col] or  'DATE' in types[col] or 'TIMESTAMP' in types[col]:
                        op_copy += "'{}', ".format(row[col])
                    else:
                        op_copy += f"{row[col]}, "
                op_copy = op_copy[:-2]
                op_copy += "), ("
            op_copy = op_copy[:-3]
            cursor.execute(op_copy)
        # adding close of cursor which I didn't see before
        cursor.close()
        connection.close()
