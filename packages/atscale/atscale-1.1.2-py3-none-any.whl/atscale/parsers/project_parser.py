from datetime import datetime
from typing import Dict, List

from atscale.parsers import parser

# the built in datetime.fromisoformat seems to fail so manually writing an iso format constant
isoformat = '%Y-%m-%dT%H:%M:%S.%f%z'


def parse_engineid_for_project(project_dict: dict) -> str:
    # make sure annotations exist
    tmp = project_dict.get("annotations", {})
    tmp = tmp.get("annotation", [])
    if len(tmp) < 1 :
        return None

    # if both annotations and annotation exists we can index them to get engineId
    for annotation in project_dict['annotations']['annotation']:
        # We're under the impression that a project only ever has one engineID
        # and the published projects refer to that. Therefore, we return the
        # first one we find.
        if annotation.get('name') == 'engineId':
            return annotation.get('value')
    return None


def parse_published_project_by_id(published_project_list: list, published_project_id: str) -> dict:
    return parser.parse_dict_list(published_project_list, 'id', published_project_id)


def parse_published_project_by_name(published_project_list: list, published_project_name: str) -> dict:
    return parser.parse_dict_list(published_project_list, 'name', published_project_name)


def parse_published_projects_for_project(project_dict: dict, published_project_list: list) -> list:
    project_engine_id = parse_engineid_for_project(project_dict)
    filtered_published_projects = []
    for published_project in published_project_list:
        if published_project['linkedProjectId'] == project_engine_id:
            filtered_published_projects.append(published_project)
    return filtered_published_projects


def parse_most_recent_published_project(published_project_list: list) -> dict:
    if published_project_list is None or len(published_project_list) < 1:
        return {}
    # start with the first published project
    published_project = published_project_list[0]
    num_pubs = len(published_project_list)
    if num_pubs < 2:
        return published_project
    publish_date = datetime.strptime(
        published_project['publishedAt'], isoformat)
    for i in range(1, num_pubs, 1):
        tmp_project = published_project_list[i]
        tmp_date = datetime.strptime(tmp_project.get('publishedAt'), isoformat)
        if tmp_date is not None and tmp_date > publish_date:
            publish_date = tmp_date
            published_project = tmp_project
    return published_project


def parse_most_recent_published_project_for_project(project_dict: dict, published_project_list: list) -> dict:
    # mashup of the two functions above this
    filtered_published_project_list = parse_published_projects_for_project(
        project_dict, published_project_list)
    return parse_most_recent_published_project(filtered_published_project_list)


def verify_published_project_dict_against_project_dict(project_dict: dict, published_project_dict: dict) -> bool:
    engine_id = parse_engineid_for_project(project_dict)
    if published_project_dict.get('linkedProjectId') == engine_id:
        return True
    else:
        return False


##############
# Data Model Stuff#
##############


def get_cube_from_published_project(published_project_dict: dict, cube_id: str):
    cubes = published_project_dict.get('cubes')
    if cubes is None:
        return None
    for cube in cubes:
        if cube.get('id') == cube_id:
            return cube
    return None


def get_cubes(project_dict: dict) -> list:
    """Grabs all cubes from a project 
    Args:
        project (dict): a complete draft project specification
    Returns:
        list:  List of all cubes(dict object) in the project, may be empty if none are found.
    """
    cubes = project_dict.setdefault('cubes', {})
    cube = cubes.setdefault('cube', [])
    return cube


def get_cube(project_dict: dict, id: str) -> dict:
    """Searches the project dict to retrieve the cube associated with the provided id. 

    Args:
        project (dict): draft project dict
        id (str): id for the cube to retrieve

    Returns:
        dict: dict for the cube for the provided id or None if one isn't found. 
    """
    cubes = get_cubes(project_dict)
    for cube in cubes:
        if cube.get('id') == id:
            return cube
    return {}


def get_perspectives(project_dict: dict) -> list:
    """ Gets all perspectives from a project as a list of dictionaries.
    Args:
        project (dict): a complete draft project specification.
    Returns:
        list: list of perspectives, may be empty if none are found.
    """
    perspectives = project_dict.setdefault('perspectives', {})
    perspective = perspectives.setdefault('perspective', [])
    return perspective


def get_perspective(project_dict: dict, id: str) -> dict:
    """Searches the project dict to retrieve the cube associated with the provided id. 

    Args:
        project (dict): draft project dict
        id (str): id for the perspective to retrieve

    Returns:
        dict: dict for the perspective for the provided id or None if one isn't found. 
    """
    perspectives = get_perspectives(project_dict)
    for perspective in perspectives:
        if perspective.get('id') == id:
            return perspective
    return {}


def get_data_models(project_dict: dict) -> list:
    """Return all data models (cubes or perspectives) associated with a project. 

    Args:
        project (dict): the dict representation of a project. 

    Returns:
        list: all data models associated with a project, may be empty if none are found. 
    """
    return get_cubes(project_dict) + get_perspectives(project_dict)


def get_data_model(project_dict: dict, id: str) -> dict:
    data_models = get_data_models(project_dict)
    for data_model in data_models:
        if data_model.get('id') == id:
            return data_model
    return {}


def get_datasets(project_dict: dict) -> list:
    """Grabs the datasets out of a project dict. 

    Args:
        project_dict (dict): a dict describing a project

    Returns:
        list: list of dictionaries, each describing a dataset
    """
    if project_dict is None:
        return []
    ds_dict = project_dict.setdefault('datasets', {})
    return ds_dict.setdefault('data-set', [])


def get_dataset_from_datasets(project_datasets: list, dataset_id: str) -> dict:
    if len(project_datasets) < 1:
        return {}
    for dataset in project_datasets:
        if dataset.get('id') == dataset_id:
            return dataset
    return {}

def _get_calculated_members(project_dict: dict) -> List[Dict]  :
    """Grabs the calculated members out of a project dict. 

    Args:
        project_dict (dict): a dict describing a calculated members

    Returns:
        list: list of dictionaries describing the calculated members
    """
    if project_dict is None:
        return []
    mem_dict = project_dict.setdefault('calculated-members', {})
    return mem_dict.setdefault('calculated-member', [])

def get_dataset_for_project_info(project_datasets: list, connection_id, schema, table_name) -> dict:
    for ds in project_datasets:
        if ds['physical']['connection']['id'] == connection_id \
                and 'tables' in ds['physical'] \
                and ds['physical']['tables'][0]['schema'] == schema \
                and ds['physical']['tables'][0]['name'] == table_name:
            return ds
    return {}


def get_dataset_from_datasets_by_name(project_datasets: list, dataset_name: str) -> dict:
    if len(project_datasets) < 1:
        return {}
    for dataset in project_datasets:
        if dataset.get('name') == dataset_name:
            return dataset
    return {}


def get_dataset_from_project_dict(project_dict: dict, dataset_id: str) -> dict:
    datasets = get_datasets(project_dict)
    return get_dataset_from_datasets(datasets, dataset_id)


def get_connection_by_id(connections: list, connection_id: str):
    for con in connections:
        if con.get('connectionId') == connection_id:
            return con
    return {}


def get_connection_list_for_project_datasets(project_datasets: list, connections: list) -> list:
    """Finds the connection associated with each project_data set and constructs a list of them in the same order
    such that project_dataset[i] references connections[i]. Note, connections may repeat in the returned list as
    more than one project dataset may refer to the same connection.

    Args:
        project_datasets (list): project data sets
        connections (list): connection group connections from the org

    Returns:
        list: a list of connections corresponding to each data set in project_datasets
    """
    project_connections = []
    for project_dataset in project_datasets:
        # If these indexes don't exist somethign went wrong, will trigger an exception
        conn_id = project_dataset['physical']['connection']['id']
        project_connections.append(get_connection_by_id(connections, conn_id))
    return project_connections


def find_dataset_with_table(datasets: list,  table_name: str) -> str:
    """Looks through the provided datasets for one that contains the given table_name

    Args:
        datasets (_type_): _description_
        table_name (_type_): _description_

    Returns:
        str: the dataset id for the first dataset found in the datasets list that contains the provided table. None if none are found. 
    """
    for ds in datasets:
        dataset_id = ds.get('id')
        phys = ds.get('physical')
        if phys:
            tables = phys.get('tables')
            if tables:
                for table in tables:
                    if table.get('name') == table_name:
                        return dataset_id
    return None
