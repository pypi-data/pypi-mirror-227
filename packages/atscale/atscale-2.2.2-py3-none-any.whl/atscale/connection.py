import getpass
import json
import logging
from typing_extensions import Final
from typing import Dict, Optional, List
import cryptocode
import requests
from html import unescape
import re
from atscale.utils.enums import RequestType
from atscale.atscale_errors import UserError
from atscale.utils import request_utils
from atscale.utils.input_utils import choose_id_and_name_from_dict_list

logger = logging.getLogger(__name__)


class Connection:
    """An object responsible for the fundamental level of connection and communication to AtScale in the explicit
    realm of a user and an organization."""


    def __init__(self, server: str, username: str, password: Optional[str] = None, organization: Optional[str] = None,
                 design_center_server_port: str = '10500', engine_port: str = '10502'):
        """Instantiates a Connection to an AtScale server given the associated parameters. After instantiating,
        Connection.connect() needs to be called to attempt to establish and store the connection.

        Args:
            server (str): The address of the AtScale server. Be sure to exclude any accidental / or : at the end
            username (str): The username to log in with.
            password (str, optional): The password to log in with. Leave as None to prompt upon calling connect().
            organization (str, optional): The organization id to work in. Can be set later by calling select_org()
                which will list all and prompt or set automatically if the user only has access to one organization.
            design_center_server_port (str, optional): The connection port for the design center. Defaults to 10500.
            engine_port (str, optional): The connection port for the engine. Defaults to 1502.
        """
        # use the setter so it can throw exception if server is None
        self.server: Final[str] = server
        # use the setter so it can throw exception if username is None
        self.username: str = username
        if password:
            self._password = cryptocode.encrypt(password,'better than nothing')
        else:
            self._password = None
        self._organization: Optional[str] = organization
        self.design_center_server_port: Optional[str] = design_center_server_port
        self.engine_port: str = engine_port
        # token as private var; see: https://docs.python.org/3/tutorial/classes.html#private-variables
        self.__token: str = None

    @property
    def server(self) -> str: 
        """Getter for the server instance variable

        Returns:
            str: the server string 
        """
        return self._server

    @server.setter
    def server(self, value: str):
        """Setter for the server instance variable. Resets connection

        Args:
            value (str): the new server string
        """
        if value is None:
            raise ValueError('Must specify server.')
        # set token to none to require (re)connect
        self.__set_token(None)
        self._server = value

    @property
    def organization(self) -> str:
        """Getter for the organization instance variable

        Returns:
            str: the organization string
        """
        return self._organization

    @organization.setter
    def organization(self, value: str):
        """Setter for the organization instance variable. Resets connection if value is None

        Args:
            value (str): the new organization string. Resets connection if None
        """
        if value is None:
            # Then they will have to (re)connect to select one.
            # I figure "no connection" errors will be easier to
            # understand than those from passing in None for org
            self.__set_token(None)
        # I don't force a reconnect otherwise. The REST API will
        # respond with errors if the user associated with token
        #Doesn't have access to the set organization.
        self._organization = value

    @property
    def username(self) -> str:
        """Getter for the username instance variable

        Returns:
            str: the username string
        """
        return self._username

    @username.setter
    def username(self, value:str):
        """The setter for the username instance variable. Resets connection

        Args:
            value (str): the new username string
        """
        if value is None:
            raise ValueError('Must specify username.')
        # set token to none to require (re)connect
        self.__set_token(None)
        self._username = value

    @property
    def password(self) -> str:
        """The getter for the password instance variable

           Raises:
               Exception: because passwords are meant to be secure.
               """
        raise Exception(
           "Passwords cannot be retrieved.")

    @password.setter
    def password(self, value:str):
        """The setter for the password instance variable. Resets connection

        Args:
            value (str): the new password to try
        """
        if value is None:
            raise ValueError('Must specify password.')
        # set token to none to require (re)connect
        self.__set_token(None)
        self._password = cryptocode.encrypt(value,'better than nothing')

    @property
    def design_center_server_port(self) -> str:
        """Getter for the design_center_server_port instance variable

        Returns:
            str: the username string
        """
        return self._design_center_server_port

    @design_center_server_port.setter
    def design_center_server_port(self, value:str):
        """The setter for the design_center_server_port instance variable. Resets connection

        Args:
            value (str): the new username string
        """
        if value is None:
            raise ValueError('Must specify design_center_server_port.')
        # set token to none to require (re)connect
        self.__set_token(None)
        self._design_center_server_port = value

    @property
    def engine_port(self) -> str:
        """Getter for the engine_port instance variable

        Returns:
            str: the username string
        """
        return self._engine_port

    @engine_port.setter
    def engine_port(self, value:str):
        """The setter for the engine_port instance variable. Resets connection

        Args:
            value (str): the new username string
        """
        if value is None:
            raise ValueError('Must specify engine_port.')
        # set token to none to require (re)connect
        self.__set_token(None)
        self._engine_port = value

    def __set_token(self, value):
        """Private method as a convenience for maintaining headers when the token is changed.
        See https://docs.python.org/3/tutorial/classes.html#private-variables
        Args:
            value (str): the new token value
        """
        self.__token = value


    def _submit_request(self, request_type: RequestType, url: str, content_type: str = 'json', data: str = '', raises: bool=False):
        headers = request_utils.generate_headers(content_type, self.__token)
        if request_type == RequestType.GET:
            response = request_utils.get_request(url, data, headers, raises)
        elif request_type == RequestType.POST:
            response = request_utils.post_request(url, data, headers, raises)
        elif request_type == RequestType.PUT:
            response = request_utils.put_request(url, data, headers, raises)
        elif request_type == RequestType.DELETE:
            response = request_utils.delete_request(url, data, headers, raises)
        else:
            raise Exception('Invalid request type')
        # If we get a 401 reauth and try again else just do the normal check response flow
        if response.status_code == 401:
            logger.info('Token expired reautherizing')
            self._auth()
            self._submit_request(request_type, url, content_type, data, raises=True)
        return request_utils.check_response(response)


    def connect(self):
        """Connects to atscale server using class variables necessary for authentication (which can be set directly or provided in constructor).
        Validates the license, stores the api token, and sets the organization. 
        May ask for user input. 
        """

        # if not self.password:
        #     self.password = getpass.getpass(prompt=f'Please enter your AtScale password for user \'{self.username}\': ')

        if self.organization is None:
            # This can still assign none to the org, in which case token will be
            # set to None in the setter for organization, and therefore this method
            # will exit but stil no token, connected() returns false. I figured those
            # errors will be easier to understand than those from passing None for org to urls
            self._select_org_pre_auth()
        self._auth()
        self._validate_license()


    def _auth(self):
        # https://documentation.atscale.com/2022.1.0/api/authentication
        header = request_utils.generate_headers()
        url = f'{self.server}:{self.design_center_server_port}/{self.organization}/auth'
        if self._password:
            password = cryptocode.decrypt(self._password, 'better than nothing')
        else:
            password = getpass.getpass(prompt=f'Please enter your AtScale password for user \'{self.username}\': ')
        response = requests.get(url, headers=header, auth=requests.auth.HTTPBasicAuth(self.username, password))
        if response.ok:
            self.__set_token(response.content.decode())
        elif response.status_code == 401:
            self._password = None
            raise UserError(response.text)
        else:
            self._password = None
            resp = json.loads(response.text)
            raise Exception(resp['response']['error'])

    def _validate_license(self):
        response = self._submit_request(request_type=RequestType.GET, url=f'{self.server}:{self.engine_port}/version')
        engine_version_string = response.text
        engine_version = float(engine_version_string.split('.')[0] + '.' + engine_version_string.split('.')[1])

        response = self._submit_request(request_type=RequestType.GET, url=f'{self.server}:{self.engine_port}/license/capabilities')
        resp = json.loads(response.text)
        if 'query_rest' not in resp['response']['content']['features'] \
                or resp['response']['content']['features']['query_rest'] is False:
            logger.warning('Query REST Endpoint not licensed for your server. You will be unable to query through AI-Link')
        if engine_version >= 2022.2:
            if 'data_catalog_api' not in resp['response']['content']['features'] \
                    or resp['response']['content']['features']['data_catalog_api'] is False:
                logger.warning('Data Catalog not licensed for your server. You may have issues pulling metadata')
        if 'ai-link' not in resp['response']['content']['features'] \
                or resp['response']['content']['features']['ai-link'] is False:
            self.__set_token(None)
            raise Exception('AI-Link not licensed for your AtScale server')

    def connected(self) -> bool:
        """Convenience method to determine if this object has connected to the server and authenticated. 
        This is determined based on whether a token has been stored locally after a connection with the
        server. 

        Returns:
            boolean: whether this object has connected to the server and authenticated.
        """
        if self.__token is not None:
            return True
        else:
            return False

    def get_orgs(self) -> List[dict]:
        """Get a list of metadata for all organizations available to the connection.

        Returns:
            list(dict): a list of dictionaries providing metadata per organization
        """
        if not self.connected():
            raise UserError('Please establish a connection by calling connect() first.')

        # The current API docs are a bit off in the response descriptions so leaving out of docstring
        # https://documentation.atscale.com/2022.1.0/api-ref/organizations
        url = f'{self.server}:{self.design_center_server_port}/api/1.0/org'
        # submit request, check for errors which will raise exceptions if there are any
        response = self._submit_request(request_type=RequestType.GET, url=url)
        # if we get down here, no exceptions raised, so parse response
        return json.loads(response.content)['response']

    def _get_orgs_for_all_users(self):
        url = f'{self.server}:{self.design_center_server_port}/login'
        resp = self._submit_request(request_type=RequestType.GET, url=url)
        match = re.search('window\.organizations = (.*?]);', str(resp.content))
        match = match[1]
        match = unescape(match).encode('utf-8').decode('unicode_escape')
        org_list = json.loads(match)
        return org_list

    def select_org(self):
        """Uses an established connection to enable the user to select from the orgs they have access to. 
        This is different from setting the organization directly, for which there is a property and associated
        setter. 

        Raises:
            UserError: error if there is no connection already established
        """
        orgs = self.get_orgs()
        if len(orgs) == 1:  # if there's only one org, let's just default to that
            self.organization = orgs[0]['id']
        else:  # if thre's more than one, then let the user pick
            org = choose_id_and_name_from_dict_list(orgs, 'Please choose an organization:')
            if org is not None:
                self.organization = org['id']

    def _select_org_pre_auth(self):
        """ Same as select_org but will list all organizations regardless of user access"""
        orgs = self._get_orgs_for_all_users()
        org = choose_id_and_name_from_dict_list(dcts=orgs, prompt='Please choose an organization:')
        if org is not None:
            self.organization = org['id']
        else:
            raise UserError('An organization must be selected before authentication occurs.')

    def _connection_groups_endpoint(self) -> str:
        return f'{self.server}:{self.engine_port}/connection-groups/orgId/{self.organization}'

    def _published_project_list_endpoint(self, suffix: str = ''):
        return f'{self.server}:{self.engine_port}/projects/published/orgId/{self.organization}{suffix}'

    def _design_org_endpoint(self, suffix: str = ''):
        return f'{self.server}:{self.design_center_server_port}/api/1.0/org/{self.organization}{suffix}'

    def _query_view_endpoint(self, suffix: str = '', limit: int = 21):
        """ Returns the query viewing endpoint with the suffix appended"""
        return f'{self.server}:{self.engine_port}/queries/orgId/{self.organization}' \
               f'?limit={limit}&userId={self.username}{suffix}'

    def _warehouse_endpoint(self, suffix: str = ''):
        return f'{self.server}:{self.engine_port}/data-sources/orgId/{self.organization}{suffix}'

    def _expression_eval_endpoint(self, suffix: str):
        return f'{self.server}:{self.engine_port}/expression-evaluator/evaluate/orgId/{self.organization}{suffix}'

    def _dmv_query_endpoint(self, suffix: str = ''):
        return f'{self.server}:{self.engine_port}/xmla/{self.organization}{suffix}'

    def _get_connection_groups(self)->list:
        u = self._connection_groups_endpoint()
        # this call will handle or raise any errors
        tmp = self._submit_request(request_type=RequestType.GET, url=u)
        # bunch of parsing I'm just going to wrap in a try and if any o fit fails I'll log and raise
        try:
            content = json.loads(tmp.content)
            if content['response']['results'].setdefault('count', 0) < 1:
                raise UserError('No connection groups found')
            return content['response']['results']['values']
        except UserError as err:
            logger.exception("no connection groups found in _get_connection_groups")
            raise
        except:
            logger.exception("couldn't parse connection groups")
            raise Exception("Error encountered while parsing connection groups.")

    def _get_published_projects(self):
        url = self._published_project_list_endpoint()
        # submit request, check for errors which will raise exceptions if there are any
        response = self._submit_request(request_type=RequestType.GET, url=url)
        # if we get down here, no exceptions raised, so parse response
        return json.loads(response.content)['response']

    def _get_projects(self):
        """See https://documentation.atscale.com/2022.1.0/api-ref/projects#projects-list-all
        Grabs projects using organiation information this object was initialized with. I believe this 
        will only return unpublished projects since it indicates full json is returned and that doesn't
        happen with published projects. 

        Raises:
            Exception: 

        Returns:
            json: full json spec of any projects
        """
        # construct the request url
        url = self._design_org_endpoint('/projects')
        # submit request, check for errors which will raise exceptions if there are any
        response = self._submit_request(request_type=RequestType.GET, url=url)
        # if we get down here, no exceptions raised, so parse response
        resp = json.loads(response.content)['response']
        return resp

    def _get_draft_project_dict(self, draft_project_id: str) -> dict:
        """Get the draft project json and convert to a dict. 

        Args:
            draft_project_id (str): The id for the draft project (i.e. not published project) to be retrieved.

        Raises:
            UserError: If there is no connection this error will be raised. 
            Exception: If there is some other problem communicating with the atscale instance an exception may be raised

        Returns:
            dict: the dict representation of the draft project, or None if no project exists for the provided draft_project_id
        """
        # construct the request url
        url = self._design_org_endpoint(f'/project/{draft_project_id}')
        response = self._submit_request(request_type=RequestType.GET, url=url)
        return json.loads(response.content)['response']

    # hitting endpoints

    def _post_query(self, query, project_name, useAggs=True, genAggs=False, fakeResults=False,
                   useLocalCache=True, useAggregateCache=True, timeout=2):
        """ Submits an AtScale SQL query to the AtScale server and returns the http requests.response object.

        :param str query: The query to submit.
        :param bool useAggs: Whether to allow the query to use aggs. Defaults to True.
        :param bool genAggs: Whether to allow the query to generate aggs. Defaults to False.
        :param bool fakeResults: Whether to use fake results. Defaults to False.
        :param bool useLocalCache: Whether to allow the query to use the local cache. Defaults to True.
        :param bool useAggregateCache: Whether to allow the query to use the aggregate cache. Defaults to True.
        :param int timeout: The number of minutes to wait for a response before timing out. Defaults to 2.
        :return: A response with a status code, text, and content fields.
        :rtype: requests.response
        """
        json_data = json.dumps(
            request_utils.generate_query_for_post(query =query, project_name = project_name,organization= self.organization,
                                                  useAggs = useAggs,genAggs =  genAggs, fakeResults = fakeResults, 
                                                  useLocalCache = useLocalCache,useAggregateCache= useAggregateCache,
                                                  timeout= timeout))
        response = self._submit_request(request_type=RequestType.POST,
            url=f'{self.server}:{self.engine_port}/query/orgId/{self.organization}/submit',
            data=json_data)
        return response


    def get_connected_warehouses(self) -> List[Dict]:
        """Returns metadata on all warehouses visible to the connection

        Raises:
            UserError: If no connection established.

        Returns:
            List[Dict]: The list of available warehouses 
        """
        if not self.connected():
            raise UserError('Please establish a connection by calling connect() first.')

        connectionGroups = self._get_connection_groups()
        
        output_list = []
        result_keys = ['name', 'platformType', 'connectionId', 'database']
        result_key_map = {x: ('warehouse_id' if x == 'connectionId' else x) for x in result_keys}

        for warehouse in connectionGroups:
            output_list.append({result_key_map[res_key]: warehouse[res_key] for res_key in result_keys})
        return output_list
        

    def get_tables(self, warehouse_id: str, database: str = None, schema: str = None) -> List[str]:
        """Get a list of available tables.

        Args:
            warehouse_id (str): The atscale warehouse to use.
            database (str, optional): The database to use. Defaults to None to use default database
            schema (str, optional): The schema to use. Defaults to None to use default schema

        Returns:
            List[str]: The list of available tables
        """
        
        if not self.connected():
            raise UserError('Please establish a connection by calling connect() first.')
        
        u = f'{self.server}:{self.engine_port}/data-sources/orgId/{self.organization}/conn/{warehouse_id}/tables/cacheRefresh'
        response = self._submit_request(request_type=RequestType.POST, url=u, data='')

        info = ''
        if database:
            info = '?database=' + database
        if schema:
            if info == '':
                info = '?schema=' + schema
            else:
                info = f'{info}&schema={schema}'
        u = f'{self.server}:{self.engine_port}/data-sources/orgId/{self.organization}/conn/{warehouse_id}/tables{info}'
        response = self._submit_request(request_type=RequestType.GET, url=u)
        return json.loads(response.content)['response']


    def get_table_columns(self, warehouse_id: str, table_name: str, database: str = None, schema: str = None) -> List[str]:
        """Get all columns in a given table

        Args:
            warehouse_id (str): The atscale warehouse to use.
            table_name (str): The name of the table to use.
            database (str, optional): The database to use. Defaults to None to use default database
            schema (str, optional): The schema to use. Defaults to None to use default schema

        Returns:
             List[str]: The columns of the passed table
        """
        if not self.connected():
            raise UserError('Please establish a connection by calling connect() first.')

        u = f'{self.server}:{self.engine_port}/data-sources/orgId/{self.organization}/conn/{warehouse_id}/tables/cacheRefresh'
        self._submit_request(request_type=RequestType.POST, url=u, data='')

        url = f'{self._warehouse_endpoint()}/conn/{warehouse_id}/table/{table_name}/info'
        if database:
            url += f'?database={database}'
            if schema:
                url += f'&schema={schema}'
        elif schema:
            url += f'?schema={schema}'
        response = self._submit_request(request_type=RequestType.GET, url=url)
        table_columns = [(x['name'], x['column-type']['data-type']) for x in
                        json.loads(response.content)['response']['columns']]
        return table_columns