import json
import uuid
from typing import List, Tuple

from atscale.errors import atscale_errors
from atscale.connection.connection import Connection
from atscale.parsers import data_model_parser, project_parser
from atscale.base import templates
from atscale.base.enums import RequestType


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
    response = atconn._submit_request(request_type=RequestType.POST,
                                      url=u, data=json.dumps(project_dict))
    project_dict = json.loads(response.content)['response']
    # now we'll use the values to construct a python Project class
    project_id = project_dict.get('id')

    from atscale.project.project import Project
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
    response = atconn._submit_request(
        request_type=RequestType.GET, url=f'{url}/clone')
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


def get_project_warehouse(project_dict: dict) -> str:
    datasets = project_parser.get_datasets(project_dict)
    warehouse_id = None
    if len(datasets) > 0:
        physicalList = datasets[0].get('physical')
        if physicalList:
            warehouse_id = physicalList.get('connection')
    return warehouse_id['id']


def create_dataset_columns_from_atscale_table_columns(table_columns: list) -> list:
    """Takes information about table columns as formatted by atscale and formats them for reference in a dataset specification.

    Args:
        table_columns (list): a list of table columns formatted as referenced by atscale

    Returns:
        list: a list of python dictionaries that represent table columns formatted for use in an atscale data set. 
    """
    columns = []
    for (name, d_type) in table_columns:
        column = templates.create_column_dict(name=name,
                                              data_type=d_type)
        columns.append(column)
    return columns


def add_dataset(project_dict, dataset):
    # setdefault only sets the value if it is currently None
    project_dict['datasets'].setdefault('data-set', [])
    project_dict['datasets']['data-set'].append(dataset)


def create_dataset(table_name: str, warehouse_id: str, table_columns: list, database: str = None, schema: str = None):
    columns = create_dataset_columns_from_atscale_table_columns(table_columns)
    dataset_id = str(uuid.uuid4())
    dataset = templates.create_dataset_dict(dataset_id=dataset_id, dataset_name=table_name,
                                            warehouse_id=warehouse_id, columns=columns,
                                            schema=schema, database=database)
    return dataset, dataset_id


def create_queried_dataset(name: str,
                           query: str,
                           columns: List[Tuple[str, str]],
                           warehouse_id: str,
                           allow_aggregates: bool):
    """ Takes your favorite name, a fancy sql expression, columns as returned by connection.get_query_columns(), and the
    warehouse_id of the connected warehouse to query against.

    Args:
        name(str): The display and query name of the dataset
        query(str): A valid SQL expression with which to directly query the warehouse of the given warehouse_id.
        warehouse_id(str): The warehouse id of the warehouse this qds and its project are pointing at.
        allow_aggregates(bool): Whether or not aggregates should be built off of this QDS.

    Returns:
        dict: The dict to append to project_dict['datasets']['dataset']
        """
    column_dict_list = create_dataset_columns_from_atscale_table_columns(
        table_columns=columns)
    return {
        'id': str(uuid.uuid4()),
        'name': name,
        'properties': {
            'allow-aggregates': allow_aggregates,
            'aggregate-locality': None,
            'aggregate-destinations': None},
        'physical': {
            'connection': {
                'id': warehouse_id},
            'queries': [{
                'sqls': [{
                    'expression': query}]}],
            'immutable': False,
            'columns': column_dict_list
        },
        'logical': {}
    }

def create_calculated_column(atconn:Connection, project_dict:dict, data_model_id:str, dataset_name: str, column_name: str, expression: str):
    """Creates a new calculated column. See AtScale documentation for more info on calculated columns.

    Args:
        data_model (DataModel): The AtScale Data Model the calculated column will exist in.
        dataset_name (str): The dataset the calculated column will be derived in.
        column_name (str): The name of the column.
        expression (str): The SQL expression for the column.
        publish (bool): Whether or not the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: If the given dataset or column does not exist in the data model
    """
    cube_dict = project_parser.get_cube(
        project_dict=project_dict, id=data_model_id)

    dset = project_parser.get_dataset_from_datasets_by_name(
        project_datasets=data_model_parser.get_project_datasets_referenced_by_cube(project_dict=project_dict,
                                                                                   cube_dict=cube_dict),
        dataset_name=dataset_name)
    if not dset:
        raise atscale_errors.UserError(f'Invalid parameter: dataset name {dataset_name} does not exist or is not '
                                       f'used in the data model yet')

    add_calculated_column_to_project_dataset(atconn=atconn, data_set=dset, column_name=column_name, expression=expression)



def add_calculated_column_to_project_dataset(atconn: Connection, data_set: dict, column_name: str, expression: str):
    """Mutates the provided data_set by adding a calculated column based on the provided column_name and expression.  

    Args:
        atconn (Connection): an AtScale connection
        data_set (dict): the data set to be mutated
        column_name (str): the name of the new calculated column
        expression (str): the sql expression that will create the values for the calculated column 
    """
    conn = data_set['physical']['connection']['id']
    table = data_set['physical']['tables'][0]
    table_name = table['name']
    database = table['database']
    schema = table['schema']

    url = atconn._expression_eval_endpoint(
        suffix=f'/conn/{conn}/table/{table_name}')
    data = {
        'dbschema': schema,
        'expression': expression,
        'database': database}
    response = atconn._submit_request(
        request_type=RequestType.POST, url=url, data=data, content_type='x-www-form-urlencoded')

    resp = json.loads(response.text)
    data_type = resp['response']['data-type']  # TODO: test for all data-types

    new_column = templates.create_column_dict(name=column_name,
                                    expression=expression,
                                    data_type=data_type)

    data_set['physical'].setdefault('columns', [])
    data_set['physical']['columns'].append(new_column)
