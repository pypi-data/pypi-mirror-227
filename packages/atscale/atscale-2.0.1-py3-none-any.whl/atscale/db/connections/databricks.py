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
        connect_args = {
            'http_path': self._http_path}
        url = self._get_connection_url()
        self._engine = create_engine(url, connect_args)
        return self._engine

    def _get_connection_url(self):
        if not self._token:
            self._token = cryptocode.encrypt(getpass.getpass(prompt='Please enter your Databricks token: '), self.platform_type.value)
        token = cryptocode.decrypt(self._token, self.platform_type.value)
        return f'databricks+connector://token:{token}@{self._host}:{self._port}/{self._schema}'


    def write_df_to_db(self, table_name: str, dataframe: DataFrame, if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL, chunksize: int = 1000):
        with self.engine.connect() as connection:
            dataframe.to_sql(name=table_name, con=connection, schema=self._schema, method='multi', index=False,
                             chunksize=chunksize, if_exists=if_exists.value)
