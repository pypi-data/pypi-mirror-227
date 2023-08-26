import getpass
import cryptocode
from pandas import DataFrame

from atscale.atscale_errors import AtScaleExtrasDependencyImportError
from atscale.db.sql_connection import SQLConnection
from atscale.utils.enums import PlatformType, TableExistsActionType

#D
class Redshift(SQLConnection):
    """The child class of SQLConnection whose implementation is meant to handle 
        interactions with a Redshift DB. 
    """

    platform_type: PlatformType = PlatformType.REDSHIFT
#D
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

        if None in [username, host, database, schema, port]:
            raise ValueError(
                'One or more of the required parameters are None.')

        self._username = username
        self._host = host
        self._database = database
        self._schema = schema
        self._port = port
        if password:
            self._password = cryptocode.encrypt(password,self.platform_type.value)
        else:
            self._password = None        
        self._engine = None

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        SQLConnection.dispose_engine(self)

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value):
        self._host = value
        SQLConnection.dispose_engine(self)

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, value):
        self._database = value
        SQLConnection.dispose_engine(self)

    @property
    def schema(self) -> str:
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value
        SQLConnection.dispose_engine(self)

    @property
    def port(self) -> str:
        return self._port

    @port.setter
    def port(self, value):
        self._port = value
        SQLConnection.dispose_engine(self)

    # @property
    # def password(self) -> str:
    #     return self._password

    # @password.setter
    # def password(self, value):
    #     self._password = value
    #     SQLConnection.dispose_engine(self)

    @property
    def password(self) -> str:
        raise Exception(
           "Passwords cannot be retrieved.")

    @password.setter
    def password(self, value):
        self._password = cryptocode.encrypt(value,self.platform_type.value)
        SQLConnection.dispose_engine(self)

    @property
    def engine(self):
        if self._engine is not None:
            return self._engine
        from sqlalchemy import create_engine
        url = self._get_connection_url()
        self._engine = create_engine(url)
        # the following line fixes a bug, not sure if the cause is sqlalchemy, sqlalchemy-redshift, or redshift-connector
        # probably should try to remove when sqlalchemy 2.0 is released
        self._engine.dialect.description_encoding = None
        return self._engine

    @engine.setter
    def engine(self, value):
    #    SQLConnection.dispose_engine(self)
    #    self._engine = value
        raise Exception(
            "It is not possible to set the engine. Please dispose, set parameters, then reference engine insead.")

    def _get_connection_url(self):
        if not self._password:
    #        self._password = getpass.getpass(prompt='Please enter your password for password: ')
            self._password = cryptocode.encrypt(getpass.getpass(prompt='Please enter your password for Redshift: '),self.platform_type.value)
        password = cryptocode.decrypt(self._password,self.platform_type.value)
    #    connection_url = f'redshift+redshift_connector://{self._username}:{self._password}@{self._host}:{self._port}/{self._database}'
        connection_url = f'redshift+redshift_connector://{self._username}:{password}@{self._host}:{self._port}/{self._database}'
        return connection_url

    def write_df_to_db(self, table_name: str, dataframe: DataFrame, if_exists: TableExistsActionType = TableExistsActionType.FAIL, chunksize: int = 1000):
        with self.engine.connect() as connection:
            dataframe.to_sql(name=table_name, con=connection, schema=self._schema, method='multi', index=False,
                             chunksize=chunksize, if_exists=if_exists.value)
