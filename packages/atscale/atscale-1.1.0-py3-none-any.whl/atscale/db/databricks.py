from pandas import DataFrame
import cryptocode
import getpass
from atscale.atscale_errors import AtScaleExtrasDependencyImportError
from atscale.db.sql_connection import SQLConnection
from atscale.utils.enums import PlatformType, TableExistsActionType

#D
class Databricks(SQLConnection):
    """The child class of SQLConnection whose implementation is meant to handle 
        interactions with Databricks. 
    """
    platform_type: PlatformType = PlatformType.DATABRICKS
#D
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
        try:
            from sqlalchemy import create_engine
        except ImportError as e:
            raise AtScaleExtrasDependencyImportError('databricks', str(e))

        if None in [host, schema, http_path, port]:
            raise ValueError(
                'One or more of the required parameters are None.')
        if token:
            self._token = cryptocode.encrypt(token,self.platform_type.value)
        else:
            self._token = None
        self._host = host
        self._schema = schema
        self._http_path = http_path
        self._port = port
        self._engine = None

    # @property
    # def token(self) -> str:
    #     return self._token

    # @token.setter
    # def token(self, value):
    #     self._token = value
    #     SQLConnection.dispose_engine(self)

    @property
    def token(self) -> str:
        raise Exception(
           "Token cannot be retrieved.")

    @token.setter
    def token(self, value):
        self._token = cryptocode.encrypt(value,self.platform_type.value)
        SQLConnection.dispose_engine(self)

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value):
        self._host = value
        SQLConnection.dispose_engine(self)

    @property
    def schema(self) -> str:
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value
        SQLConnection.dispose_engine(self)

    @property
    def http_path(self) -> str:
        return self._http_path

    @http_path.setter
    def http_path(self, value):
        self._http_path = value
        SQLConnection.dispose_engine(self)

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value):
        self._port = value
        SQLConnection.dispose_engine(self)

    @property
    def engine(self):
        if self._engine is not None:
            return self._engine
        from sqlalchemy import create_engine
        connect_args = {
            'http_path': self._http_path}
        url = self._get_connection_url()
        self._engine = create_engine(url, connect_args)
        return self._engine

    @engine.setter
    def engine(self, value):
    #    SQLConnection.dispose_engine(self)
    #    self._engine = value
        raise Exception(
            "It is not possible to set the engine. Please dispose, set parameters, then reference engine insead.")

    def _get_connection_url(self):
        if not self._token:
            self._token = cryptocode.encrypt(getpass.getpass(prompt='Please enter your Databricks token: '), self.platform_type.value)
        token = cryptocode.decrypt(self._token, self.platform_type.value)
    #    return f'databricks+connector://token:{self._token}@{self._host}:{self._port}/{self._schema}'
        return f'databricks+connector://token:{token}@{self._host}:{self._port}/{self._schema}'


    def write_df_to_db(self, table_name: str, dataframe: DataFrame, if_exists: TableExistsActionType = TableExistsActionType.FAIL, chunksize: int = 1000):
        with self.engine.connect() as connection:
            dataframe.to_sql(name=table_name, con=connection, schema=self._schema, method='multi', index=False,
                             chunksize=chunksize, if_exists=if_exists.value)
