import getpass
import cryptocode
import inspect
import logging

from atscale.errors.atscale_errors import AtScaleExtrasDependencyImportError
from atscale.db.sqlalchemy_connection import SQLAlchemyConnection
from atscale.base.enums import PlatformType
from atscale.utils import validation_utils

logger = logging.getLogger(__name__)

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

        try:
            from sqlalchemy import create_engine
        except ImportError as e:
            raise AtScaleExtrasDependencyImportError('redshift', str(e))

        super().__init__()

        # ensure any builder didn't pass any required parameters as None
        local_vars = locals()
        inspection = inspect.getfullargspec(self.__init__)
        validation_utils.validate_required_params_not_none(local_vars=local_vars,
                                                           inspection=inspection)

        self._username = username
        self._host = host
        self._database = database
        self._schema = schema
        self._port = port
        if password:
            self._password = cryptocode.encrypt(password, self.platform_type.value)
        else:
            self._password = None   

        try:
            validation_connection = self.engine.connect()
            validation_connection.close()
            self.dispose_engine() 
        except:
            logger.error('Unable to create database connection, please verify the inputs')
            raise


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
        from sqlalchemy.engine import URL

        if not self._password:
            self._password = cryptocode.encrypt(getpass.getpass(prompt='Please enter your password for Redshift: '),self.platform_type.value)
        password = cryptocode.decrypt(self._password,self.platform_type.value)
        connection_url = URL.create('redshift+redshift_connector', username=self._username,
                                    password=password, host=self._host, port=self._port,
                                    database=self._database)
        return connection_url
