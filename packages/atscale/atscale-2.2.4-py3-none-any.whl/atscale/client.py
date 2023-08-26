import json
import logging
from typing import List, Dict

from pandas import DataFrame

from atscale.utils import auto_data_modeling_utils
from atscale.base import config
from atscale.connection.connection import Connection
from atscale.db.sql_connection import SQLConnection
from atscale.errors import atscale_errors
from atscale.parsers import project_parser
from atscale.project.project import Project
from atscale.utils import db_utils, input_utils, model_utils, project_utils
from atscale.base.enums import RequestType

logger = logging.getLogger(__name__)


class Client:
    """Creates a Client with a connection to an AtScale server to allow for interaction with the projects on the server.
    """

    def __init__(self, config_path: str = None, server: str = None, username: str = None, organization: str = None,
                 password: str = None, design_center_server_port: str = None, engine_port: str = None, 
                 jdbc_driver_class = 'org.apache.hive.jdbc.HiveDriver', jdbc_driver_path = ''):
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
            jdbc_driver_class (str, optional): The class of the hive jdbc driver to use. Defaults to com.cloudera.hive.jdbc.HS2Driver.
            jdbc_driver_path (str, optional): The path to the hive jdbc driver to use. Defaults to '' which will not allow querying via jdbc

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
        s, u, p, o, d, e, dc, dp = self._get_connection_parameters_from_config()
        # finally, we'll overwrite values with any they passed in
        if server is not None:
            s = server
        if username is not None:
            u = username
        if organization is not None:
            o = organization
        if password is not None:
            p = password
        if jdbc_driver_class is not None:
            dc = jdbc_driver_class
        if jdbc_driver_path is not None:
            dp = jdbc_driver_path
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
        self._atconn = Connection(s, u, p, o, d, e, dc, dp)

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
        jdbc_driver_class = cfg.get('jdbc_driver_class')
        jdbc_driver_path = cfg.get('jdbc_driver_path')
        return server, username, password, organization, design_center_server_port, engine_port, jdbc_driver_class, jdbc_driver_path

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
        response = self._atconn._submit_request(
            request_type=RequestType.POST, url=u, data=p)
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

        dbconn.write_df_to_db(table_name=table_name, dataframe=dataframe)
        # create a new, empty project and add a dataset to it
        project = self.create_empty_project(project_name) 
        project_dict = project._get_dict()
        database, schema = db_utils.get_database_and_schema(dbconn=dbconn)
        # get the table_name as atscale sees it
        atscale_table_name = db_utils.get_atscale_tablename(
            atconn=self._atconn, warehouse_id=warehouse_id, database=database, schema=schema, table_name=table_name)
        # get the columns, as atscale sees them (i.e. with the atscale types necessary for dataset specification)
        columns = self.atconn.get_table_columns(
            warehouse_id=warehouse_id, table_name=atscale_table_name, database=database, schema=schema)
        #create the data set and add it to the new, empty 
        dataset, dataset_id = project_utils.create_dataset(
            warehouse_id=warehouse_id, database=database, schema=schema, table_name=atscale_table_name, table_columns=columns)
        project_utils.add_dataset(project_dict, dataset)
        # Grab the single, default data_model from the project and add a data-set-ref to it which references the dataset we just added to the project.
        model_dict = project_parser.get_cubes(project_dict)[0]
        model_utils.add_data_set_ref(model_dict, dataset_id)
        #now we update the data_model by automatically adding any dimensions / measures we can identify 
        auto_data_modeling_utils.create_semantic_layer(atconn=self.atconn, dbconn=dbconn, table_name=atscale_table_name, project_dict=project_dict, data_model_id=model_dict.get('id'), dataset_id=dataset_id, columns=columns)
        #finally update the project using projet_dict after all the mutations from above
        project._update_project(project_json=project_dict, publish=publish)
        return project

    def get_organizations(self) -> List[Dict[str, str]]:
        """Prints all Organizations for the associated Server if possible and returns a list of dicts 
            for each of the listed organizations. List index should match printed index.

        Returns:
            List[Dict[str,str]]: List of 'id':'name' pairs of available orgs.
        """

        orgList = self.atconn._get_orgs_for_all_users()

        print('Note: Organization ID is expected in Client and Connection constructors.')
        for i, dct in enumerate(orgList):
            print("Index:{} ID: {}: Name: {}".format(
                i, dct['id'], dct['name']))

        return orgList

    def get_projects(self) -> List[Dict[str, str]]:
        """Prints all Projects that are visible for the associated Connection. Returns a list of dicts
            for each of the listed Projects. List index should match printed index.

        Returns:
            List[Dict[str,str]]: List of 'id':'name' pairs of available Projects.
        """
        if not self._atconn.connected():
            raise atscale_errors.UserError(
                'Please establish a connection by calling connect() first.')
        # projects is a list of dicts where each is a project
        projectsList = self._atconn._get_projects()

        print('Note: Project ID is expected in Project constructor.')
        for i, dct in enumerate(projectsList):
            print("Index:{} ID: {}: Name: {}".format(
                i, dct['id'], dct['name']))

        return projectsList

    def get_published_projects(self, draft_project_id: str) -> List[Dict[str, str]]:
        """Prints all Published Projects that are visible for the associated Connection for the 
            given draft project id. Returns a list of dicts for each of the listed Projects. List
            index should match printed index.
        Args:
            draft_project_id (str): The id of the draft project of interest
        Returns:
            List[Dict[str,str]]: List of 'id':'name' pairs of available published Projects.
        """
        from atscale.utils.project_utils import project_parser

        if not self._atconn.connected():
            raise atscale_errors.UserError(
                'Please establish a connection by calling connect() first.')

        draft_project_dict = self._atconn._get_draft_project_dict(
            draft_project_id)

        published_project_list = self._atconn._get_published_projects()

        specific_published_projects_list = project_parser.parse_published_projects_for_project(
            draft_project_dict, published_project_list)

        if not published_project_list:
            raise atscale_errors.UserError(
                'There is no published version of this project')

        print('Note: Published Project ID is optional in Project constructor.')
        for i, dct in enumerate(specific_published_projects_list):
            print("Index:{} ID: {}: Name: {}".format(
                i, dct['id'], dct['name']))

        return specific_published_projects_list
