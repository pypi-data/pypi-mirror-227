import json
import logging

from pandas import DataFrame

from atscale import atscale_errors
from atscale.connection import Connection
from atscale.db.sql_connection import SQLConnection
from atscale.project import Project
from atscale.utils import db_utils, input_utils, config
from atscale.utils.enums import RequestType

logger = logging.getLogger(__name__)

class Client:
    """Creates a Client with a connection to an AtScale server to allow for interaction with the projects on the server.
    """

    def __init__(self, config_path: str = None, server: str = None, username: str = None, organization: str = None,
                 password: str = None, design_center_server_port: str = None, engine_port: str = None):
        """All parameters are optional. If none are provided, this method will attempt to use values from the following, local configuration files: 
        - ~/.atscale/config - for server, organizatoin, design_center_server_port, and engine_port
        - ~/.atscale/credentials - for username and password

        If a config_path parameter is provided, all values will be read from that file. 

        Any values provided in addition to a config_path parameter will take precedence over values read in from the file at config_path.

        Args:
            config_path (str, optional): path to a configuration file in .INI format with values for the other parameters. Defaults to None.
            server (str, optional): the atscale server instance. Defaults to None.
            username (str, optional): username. Defaults to None.
            organization (str, optional): the atscale organization id. Defaults to None.
            password (str, optional): password. Defaults to None.
            design_center_server_port (str, optional): port for atscale design center. Defaults to '10500'.
            engine_port (str, optional): port for atscale engine. Defaults to '10502'.

        Raises:
            ValueError: an error if insufficient information provided to establish a connection. 

        Returns:
            Client: an instance of this class
        """
        # Config will load default config files config.ini, ~/.atscale/config and ~/.atscale/credentials on first call to constructor.
        # It's a singleton, so subsequent calls to it's constructor will simply obtain a reference to the existing instance.
        if config_path is not None:
            cfg = config.Config()
            # Any keys in here that are already in Config will get new values from this file
            cfg.read(config_path)
        # go ahead nad grab the connection values from config
        s, u, p, o, d, e = self._get_connection_parameters_from_config()
        # finally, we'll overwrite values with any they passed in
        if server is not None:
            s = server
        if username is not None:
            u = username
        if organization is not None:
            o = organization
        if password is not None:
            p = password
        # if someone passed in a value, we'll use that (defaults to None)
        if design_center_server_port is not None:
            # If I use default value of port instead of None, then I won't know if the value here was specified
            # by the user passing it in, or if they didn't pass in the parameter and let it go to default. By using
            # None as default, I know they did not pass in a value. I want one more check if we got it from config
            d = design_center_server_port
        elif d is None:  # if the value wasn't found in the Config file, let's use the default
            d = config.DEFAULT_DESIGN_CENTER_PORT
        if engine_port is not None:
            e = engine_port
        elif e is None:
            e = config.DEFAULT_ENGINE_PORT

        # if we didn't find these values in the Config work above and they weren't passed in, then we didn't get enough info
        if s is None:
            raise ValueError(
                f"Value for server must be provided.")
        if u is None:
            raise ValueError(
                f"Value for username must be provided.")
        # otherwise we'll go ahead and make the connection object
        self._atconn = Connection(s, u, p, o, d, e)

    @property
    def atconn(self) -> Connection:
        """A property that gets the Client object's AtScale connection

        Returns:
            Connection: The Client object's AtScale connection
        """
        return self._atconn

    @atconn.setter
    def atconn(self, value):
        """The setter for the Client object's AtScale connection. This property is final; it cannot be reset

        Args:
            value (Any): The value that the user attempts to set the AtScale connection to

        Raises:
            atscale_errors.UserError: The user cannot reset the value of the AtScale connection
        """
        raise atscale_errors.UserError('The value of atconn is FINAL')

    def get_version(self) -> str:
        """A getter function for the current version of the library

        Returns:
            str: The current version of the library
        """
        return config.Config().version

    def connect(self):
        """Initializes the Client object's connection 
        """
        self._atconn.connect()

    def _get_connection_parameters_from_config(self):
        cfg = config.Config()
        # should be placed in ~/.atscale/credentials then config will grab them
        username = cfg.get('username')
        password = cfg.get('password')
        # Config reads these first from config.ini in project root and then ~/.atscale/config.
        # Would be overwritten with any values from subsequent config_path read in.
        server = cfg.get('server')
        organization = cfg.get('organization')
        design_center_server_port = cfg.get('design_center_server_port')
        engine_port = cfg.get('engine_port')
        return server, username, password, organization, design_center_server_port, engine_port

    def create_empty_project(self, project_name: str) -> Project:
        """Creates an empty project

        Args:
            project_name (str): The name of the empty project to be created

        Returns:
            Project: An empty project
        """
        # create an empty project on the atscale server
        if not self._atconn.connected():
            raise atscale_errors.UserError(
                'Please establish a connection by calling connect() first.')

        existing_projects = self.atconn._get_projects()
        if len(existing_projects) > 0:
            for x in existing_projects:
                if x['name'] == project_name:
                    raise atscale_errors.UserError(
                        'Project name already taken, new project name must be unique')

        u = self._atconn._design_org_endpoint('/project/createEmpty')
        p = {
            "name": project_name}
        p = json.dumps(p)
        # this call will handle or raise any errors
        response = self._atconn._submit_request(request_type=RequestType.POST, url=u, data=p)
        project_dict = json.loads(response.content)['response']
        # now we'll use the values to construct a python Project class
        project_id = project_dict.get('id')
        proj = Project(atconn=self._atconn, project_id=project_id)
        return proj

    def select_project(self) -> Project:
        """Selects a project based on user input

        Returns:
            Project: The desired project
        """
        if not self._atconn.connected():
            raise atscale_errors.UserError(
                'Please establish a connection by calling connect() first.')
        # projects is a list of dicts where each is a project
        projects = self._atconn._get_projects()
        # ask the user to select one of the projects, return dict result
        project_dict = input_utils.choose_id_and_name_from_dict_list(
            projects, 'Please choose a project:')
        if project_dict is None:
            return None
        id = project_dict.get('id')
        if id is None:
            logger.exception(
                "Unable to parse id from selected project in atscale_client.")
            raise Exception("Unable to retrieve ID for selected project.")
        project = Project(self._atconn, id)
        return project

    def writeto(self, dbconn: SQLConnection, warehouse_id: str, project_name: str, table_name: str, dataframe: DataFrame, publish=True) -> Project:
        if not self._atconn.connected():
            raise atscale_errors.UserError(
                'Please establish a connection by calling connect() first.')
                
        atscale_table_name, column_dict = db_utils.write_dataframe_to_db(atconn=self.atconn, dbconn=dbconn, warehouse_id=warehouse_id,
                                                                         table_name=table_name,  dataframe=dataframe)
        project = self.create_empty_project(project_name)
        data_model = project.get_data_model()
        database = None
        schema = None
        if hasattr(dbconn, 'database'):
            database = dbconn.database
        if hasattr(dbconn, 'schema'):
            schema = dbconn.schema
        data_model.add_dataset(warehouse_id=warehouse_id, database=database,
                               schema=schema, table_name=atscale_table_name, publish=publish)
        return project
