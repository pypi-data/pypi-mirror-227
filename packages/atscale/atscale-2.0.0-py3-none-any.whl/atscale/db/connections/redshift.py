import getpass
import cryptocode
import inspect
from pandas import DataFrame

from atscale.errors.atscale_errors import AtScaleExtrasDependencyImportError
from atscale.db.sql_connection import SQLConnection
from atscale.db.sqlalchemy_connection import SQLAlchemyConnection
from atscale.base.enums import PlatformType, PandasTableExistsActionType

class Redshift(SQLAlchemyConnection):
    """The child class of SQLConnection whose implementation is meant to handle 
        interactions with a Redshift DB. 
    """

    platform_type: PlatformType = PlatformType.REDSHIFT

    def __init__(self, username:str, host:str, database:str, schema:str, port:str='5439', password:str=None):
        """Constructs an instance of the Redshift SQLConnection. Takes arguments necessary to find the database 
            and schema. If password is not provided, it will prompt the user to login.

        Args:
            username (str): the username necessary for login
            host (str): the host of the intended Redshift connection
            database (str): the database of the intended Redshift connection
            schema (str): the schema of the intended Redshift connection
            port (str, optional): A port if non-default is configured. Defaults to 5439.
            password (str, optional): the password associated with the username. Defaults to None.
        """
        super().__init__()
        
        try:
            from sqlalchemy import create_engine
        except ImportError as e:
            raise AtScaleExtrasDependencyImportError('redshift', str(e))

        localVars = locals()
        inspection = inspect.getfullargspec(self.__init__)
        all_params = inspection[0]  # list of all parameters names in order (optionals must come after required)
        defaults = inspection[3]  # tuple of default values (for every optional parameter)
        param_name_list = all_params[:-len(defaults)]  # parameter has default if and only if its optional
        param_names_none = [x for x in param_name_list if localVars[x] is None]
        
        if param_names_none:
            raise ValueError(
                f'The following required parameters are None: {", ".join(param_names_none)}')

        self._username = username
        self._host = host
        self._database = database
        self._schema = schema
        self._port = port
        if password:
            self._password = cryptocode.encrypt(password,self.platform_type.value)
        else:
            self._password = None        


    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        self.dispose_engine()

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value):
        self._host = value
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
    def port(self) -> str:
        return self._port

    @port.setter
    def port(self, value):
        self._port = value
        self.dispose_engine()

    @property
    def password(self) -> str:
        raise Exception(
           "Passwords cannot be retrieved.")

    @password.setter
    def password(self, value):
        self._password = cryptocode.encrypt(value,self.platform_type.value)
        self.dispose_engine()

    @property
    def engine(self):
        if self._engine is not None:
            return self._engine
        self._engine = SQLAlchemyConnection.engine
        # the following line fixes a bug, not sure if the cause is sqlalchemy, sqlalchemy-redshift, or redshift-connector
        # probably should try to remove when sqlalchemy 2.0 is released
        self._engine.dialect.description_encoding = None
        return self._engine

    def _get_connection_url(self):
        if not self._password:
            self._password = cryptocode.encrypt(getpass.getpass(prompt='Please enter your password for Redshift: '),self.platform_type.value)
        password = cryptocode.decrypt(self._password,self.platform_type.value)
        connection_url = f'redshift+redshift_connector://{self._username}:{password}@{self._host}:{self._port}/{self._database}'
        return connection_url
