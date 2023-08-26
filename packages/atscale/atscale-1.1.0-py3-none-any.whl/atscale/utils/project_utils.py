import json
import uuid
from atscale.connection import Connection
from atscale import atscale_errors
from atscale.connection import Connection
from atscale.utils import request_utils
from atscale.parsers import project_parser
from atscale.utils import request_utils


def create_project(atconn: Connection, project_dict: dict):
    """ Creates a new project using the JSON data provided.
    :param json json_data: The JSON file to be sent to AtScale.
    :return: A project instance of the new project
    :rtype: Project
    """
    if not atconn.connected():
        raise atscale_errors.UserError(
            'Establishing a connection in the atconn field is required')
    u = atconn._design_org_endpoint('/project')
    h = atconn._generate_headers()
    response = request_utils.post_request(
        url=u, data=json.dumps(project_dict), headers=h)
    project_dict = json.loads(response.content)['response']
    # now we'll use the values to construct a python Project class
    project_id = project_dict.get('id')

    from atscale.project import Project
    return Project(atconn=atconn, project_id=project_id)


def clone_dict(atconn: Connection, original_project_id: str, new_project_name: str) -> dict:
    """makes a clone of the orginal projects dictionary with a new project name
    Args:
        original_project (Project): the orginal project to make a clone of
        new_project_name (str): the name of the clone

    Returns:
        dict: the project dict of the clone
    """

    url = f'{atconn._design_org_endpoint()}/project/{original_project_id}'
    response = request_utils.get_request(
        f'{url}/clone', headers=atconn._generate_headers())
    copy_dict = json.loads(response.content)['response']
    copy_dict['name'] = new_project_name
    copy_dict['properties']['caption'] = new_project_name

    # this method of adjusting the ids may not work if we swap get_datasets to pass by value
    original_project_dict = atconn._get_draft_project_dict(original_project_id)
    original_datasets = project_parser.get_datasets(original_project_dict)

    data_list = []
    for dataset in original_datasets:
        data_list.append(dataset['physical']['connection']['id'])
    for copy_data in copy_dict['datasets']['data-set']:
        copy_data['physical']['connection']['id'] = data_list.pop(0)

    return copy_dict


def create_dataset_columns_from_table_columns(table_columns:list)->list:
    """_summary_

    Args:
        table_columns (list): _description_

    Returns:
        list: a list of columns formatted for use in a dataset with freshly minted uuid id values.
    """
    columns = []
    for (name, d_type) in table_columns:
        column = {
            'id': str(uuid.uuid4()),
            'name': name,
            'type': {
                'data-type': d_type
            }
        }
        columns.append(column)
    return columns


def create_dataset(table_name: str, warehouse_id: str, table_columns: list, database:str=None, schema: str=None):
    columns = create_dataset_columns_from_table_columns(table_columns)

    dataset_id = str(uuid.uuid4())
    dataset = {
        'id': dataset_id,
        'name': table_name,
        'properties': {
            'allow-aggregates': True,
            'aggregate-locality': None,
            'aggregate-destinations': None
        },
        'physical': {
            'connection': {
                'id': warehouse_id
            },
            'tables': [{
                'name': table_name
            }],
            'immutable': False,
            'columns': columns
        },
        'logical': {}
    }

    if schema:
        dataset['physical']['tables'][0]['schema'] = schema
    if database:
        dataset['physical']['tables'][0]['database'] = database
    return dataset, dataset_id


def get_project_warehouse(project_dict: dict)->str:
    datasets = project_parser.get_datasets(project_dict)
    warehouse_id = None
    if len(datasets) > 0:
        physicalList = datasets[0].get('physical')
        if physicalList:
            warehouse_id = physicalList.get('connection')
    return warehouse_id['id']