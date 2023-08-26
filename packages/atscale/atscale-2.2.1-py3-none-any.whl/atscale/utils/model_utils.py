import logging
import uuid
import json
from typing import List, Dict, Tuple

from atscale.data_model.data_model import DataModel
from atscale.errors import atscale_errors
from atscale.base import enums, templates
from atscale.parsers import data_model_parser, project_parser
from atscale.utils import dimension_utils, feature_utils, project_utils, time_utils
from atscale.db.sql_connection import SQLConnection
from atscale.connection import Connection
from atscale.base import endpoints

logger = logging.getLogger(__name__)


def _add_data_set_ref(model_dict: Dict, dataset_id: str):
    """Adds a data-set-ref into the provided model_dict with the given dataset_id

    Args:
        model_dict (Dict): the dict representation of the datamodel to add the dataset to
        dataset_id (str): the id of the dataset to create
    """
    data_set_ref = templates.create_dataset_ref_dict(dataset_id)
    model_dict.setdefault('data-sets', {})
    model_dict['data-sets'].setdefault('data-set-ref', [])
    model_dict['data-sets']['data-set-ref'].append(data_set_ref)

def _check_features(features: list, check_list: list, errmsg: str = None):
    """Checks that the given feature(s) exist(s) within a specified list of features.

    Args:
        features (list): feature(s) to confirm exist in the provided list
        check_list (list): features of the data model to check against
        errmsg (str, optional): Error message to raise if feature not found. Defaults to None.
    
    Raises:
        atscale_errors.UserError: error is raised if any featuers of interest not found, can be customized via errmsg arg
    
    Returns:
        boolean: True if no error found
    """
    setDif = set(features) - set(check_list)
    if len(setDif) > 0:
        if errmsg:
            raise atscale_errors.UserError(errmsg)
        else:
            raise atscale_errors.UserError(
                f'Features: {sorted(list(setDif))} not in data model. Make sure each feature has been published and is'
                ' correctly spelled')
    return True

def _create_dataset_relationship(atconn, project_dict, cube_id, database, schema, table_name, join_features,
                                 join_columns=None,
                                 roleplay_features=None):
    """ Mutates and returns the given project_dict to create a dataset, join the given features, and join the dataset
    to the cube if it was not already.

    Args:
        atconn (Connection): A Connection object connected to the server of the project the parameters correspond to.
        project_dict (dict): The project_dict to mutate and return
        cube_id (str): The id of the cube the dataset will be joined to.
        database (str): The database that the created dataset will point at.
        schema (str): The schema that the created dataset will point at.
        table_name (str): The table that the created dataset will point at.
            This will also become the name of the dataset.
        join_features (list): a list of features in the data model to use for joining.
        join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
            None or the same length and order as join_features. Defaults to None to use identical names to the
            join_features. If multiple columns are needed for a single join they should be in a nested list
        roleplay_features (list, optional): The roleplays to use on the relationships. List must be either
            None or the same length and order as join_features. Use '' to not roleplay that relationship.
            Defaults to None.

    Returns:
        Dict: The mutated project_dict
    """
    warehouse_id = project_parser.get_project_warehouse(project_dict)
    project_datasets = project_parser.get_datasets(project_dict)

    if join_columns is None:
        join_columns = join_features

    if roleplay_features is None:
        roleplay_features = []
        for feature in join_features:
            roleplay_features.append('')

    if len(join_features) != len(join_columns):
        raise Exception(f'join_features and join_columns lengths must match. join_features is length '
                        f'{len(join_features)} while join_columns is length {len(join_columns)}')

    if roleplay_features is not None and len(join_features) != len(roleplay_features):
        raise Exception(f'join_features and roleplay_features lengths must match. join_features is length '
                        f'{len(join_features)} while roleplay_features is length {len(roleplay_features)}')

    url = endpoints._endpoint_warehouse(atconn,f'/conn/{warehouse_id}/tables/cacheRefresh')
    atconn._submit_request(request_type=enums.RequestType.POST, url=url)

    # we'll use table_columns potentially for creating a dataset below and then more logic after that
    table_columns = atconn.get_table_columns(warehouse_id=warehouse_id,
                                             table_name=table_name,
                                             database=database,
                                             schema=schema)

    # there was a check as to whether the datasets element was null which set it to an empty list. I'm not sure if that would
    # ever be possible. If so, I imagine project_datasets would have to be null, and then verify_connection would fail. If we
    # want to support this, then we'd have to change verify to not check project_data set values. I rearranged the logic a lot.
    # Figured that was safe to pull out into an independent check here.
    project_dict['datasets'].setdefault('data-set', [])

    # look for a dataset that may already have the table_name for the table we're trying to join to the cube (meaning the table
    # already exists and we're just replacing it or appending it)
    dataset_id = project_parser.find_dataset_with_table(
        project_datasets, table_name)

    if not dataset_id:  # then we have to create a project_dataset
        # the prior code assumed a schema but checked if database was None prior to setting
        project_dataset, dataset_id = project_utils.create_dataset(
            table_name, warehouse_id, table_columns, database, schema)
        # and we'll add the newly minted dataset to the project_dict
        project_utils.add_dataset(project_dict=project_dict, dataset=project_dataset)

    return _create_dataset_relationship_from_dataset(project_dict=project_dict,
                                                     cube_id=cube_id,
                                                     dataset_name=table_name,
                                                     join_features=join_features,
                                                     join_columns=join_columns,
                                                     roleplay_features=roleplay_features)

def _create_dataset_relationship_from_dataset(project_dict: dict,
                                              cube_id: str,
                                              dataset_name: str,
                                              join_features: List[str],
                                              join_columns: List[str] = None,
                                              roleplay_features: List[str]= None):
    """ Mutates and returns the given project_dict to join the given features and join the dataset, of the given name,
    to the cube (if not joined already) of the given cube_id. 

    Args:
        atconn (Connection): A Connection object connected to the server of the project the parameters correspond to.
        project_dict (dict): The project_dict to mutate and return.
        cube_id (str): The id of the cube the dataset will be joined to.
        dataset_name (str): The name of the dataset to target. This dataset must exist in project_datasets.
            This will also become the name of the dataset.
        join_features (list): a list of features in the data model to use for joining.
        join_columns (list, optional): The columns in the dataframe to join to the join_features. List must be either
            None or the same length and order as join_features. Defaults to None to use identical names to the
            join_features. If multiple columns are needed for a single join they should be in a nested list
        roleplay_features (list, optional): The roleplays to use on the relationships. List must be either
            None or the same length and order as join_features. Use '' to not roleplay that relationship. 
            Defaults to None.

    Returns:
        Dict: The mutated project_dict
        """
    if join_columns is None:
        join_columns = join_features
    elif len(join_features) != len(join_columns):
        raise Exception(f'join_features and join_columns lengths must match. join_features is length '
                        f'{len(join_features)} while join_columns is length {len(join_columns)}')

    if roleplay_features is None:
        # [''] * len() will make references to the same str
        roleplay_features = ['' for x in range(len(join_features))]
    elif roleplay_features is not None and len(join_features) != len(roleplay_features):
        raise Exception(f'join_features and roleplay_features lengths must match. join_features is length '
                        f'{len(join_features)} while roleplay_features is length {len(roleplay_features)}')

    project_datasets = project_parser.get_datasets(project_dict)
    dataset_id = project_parser.get_dataset_from_datasets_by_name(
        project_datasets=project_datasets,
        dataset_name=dataset_name)['id']

    key_refs = []
    attribute_refs = []

    joins = tuple(zip(join_features, join_columns, roleplay_features))
    cube_dict = project_parser.get_cube(project_dict, cube_id)

    # create dict from all feature name to their index in project level attributes
    feat_name_to_project_attribute: Dict[str, int] = {}
    project_keyed_attributes = project_dict.get(
        'attributes', {}).get('keyed-attribute', [])
    for index, attribute in enumerate(project_keyed_attributes):
        feat_name_to_project_attribute[attribute['name']] = index

    for join_feature, join_column, roleplay_feature in joins:
        # Questions :
        # Why are we making a list for each join feature, column, and roleplay feature?
        # Cols is a list and we set it on key_ref - can that literally be more than on column? Why is it a list? If it is a list, why is the key not cols instead of col?
        if type(join_column) != list:
            # method can take a list of [join_column] or just a list of strings
            join_column = [join_column]

        # looks in the project for an attribute that matches the join feature. If one is found,
        # it determines if user specified it as a roleplay feature. If they did, it looks for the name
        # at the current location to see if it matches the name provided by the user for the roleplay feature
        # and if that is not found, it appends the current name in place, to the provided roleplay  feature,
        # and constructs the json around it, like ref_id, and sets it up to reference the dimension id
        dimension_index = feat_name_to_project_attribute.get(join_feature)
        if dimension_index is not None:  # don't do bool because if index is 0 it will return false
            dimension = project_keyed_attributes[dimension_index]
            ref = dimension['key-ref']
            key_ref = {
                'id': ref,
                'unique': False,
                'complete': 'false',
                'column': join_column
            }
            if roleplay_feature != '':
                if '{0}' not in roleplay_feature:
                    roleplay_feature = roleplay_feature + ' {0}'
                ref_id = str(uuid.uuid4())
                ref_path = {
                    'new-ref': {
                        'attribute-id': dimension['id'],
                        'ref-id': ref_id,
                        'ref-naming': roleplay_feature
                    }
                }
                key_ref['ref-path'] = ref_path
            key_refs.append(key_ref)

        # if the join features was not found as a dimension in project_json above, look in the cube.
        if not dimension_index:
            cube_keyed_attributes = cube_dict.get(
                'attributes', {}).get('keyed-attribute', [])
            feat_name_to_cube_attribute: Dict[str, int] = {
                x['name']: i for i, x in enumerate(cube_keyed_attributes)}
            dimension_index = feat_name_to_cube_attribute.get(join_feature)
            if dimension_index is not None:
                dimension = cube_keyed_attributes[dimension_index]
                ref = dimension['key-ref']
                key_ref = {
                    'id': ref,
                    'unique': False,
                    'complete': 'partial',
                    'column': join_column
                }
                if roleplay_feature != '':
                    if '{0}' not in roleplay_feature:
                        roleplay_feature = roleplay_feature + ' {0}'
                    ref_id = str(uuid.uuid4())
                    ref_path = {
                        'new-ref': {
                            'attribute-id': dimension['id'],
                            'ref-id': ref_id,
                            'ref-naming': roleplay_feature
                        }
                    }
                    key_ref['ref-path'] = ref_path
                key_refs.append(key_ref)
                uid = dimension['id']
                attr = {
                    'id': uid,
                    'complete': 'partial',
                    'column': join_column
                }
                attribute_refs.append(attr)
    found = False
    cube_dict.setdefault('data-sets', {})
    cube_dict['data-sets'].setdefault('data-set-ref', [])
    for ds_ref in cube_dict['data-sets']['data-set-ref']:
        if ds_ref['id'] == dataset_id:
            found = True
            ds_ref['logical'].setdefault('key-ref', [])
            ds_ref['logical']['key-ref'] = ds_ref['logical']['key-ref'] + key_refs
            ds_ref['logical'].setdefault('attribute-ref', [])
            ds_ref['logical']['attribute-ref'] = ds_ref['logical']['attribute-ref'] + attribute_refs
            break

    # If we had to create a dataset for the project to point at the new table, then we need to ensure there is also one in the cube referencing it.
    # This check previously referred back to "found" which was based on the project data set being there, but this is really about whether we
    # find it in the cube, which is in the logic immediately above, so I'll do the boolean there instead.
    if not found:
        data_set_ref = templates.create_dataset_ref_dict(
            dataset_id, key_refs, attribute_refs)
        cube_dict['data-sets']['data-set-ref'].append(data_set_ref)

    return project_dict

def _get_column_type_category(column_type: str) -> str:
    """ returns the category of the given column type

    Args:
        column_type (str): the column type to look up

    Returns:
        str: the category of the column type ('categorical', 'date', or 'numeric')
    """
    type_dict = {
        'string': 'categorical',
        'char': 'categorical',
        'varchar': 'categorical',
        'nchar': 'categorical',
        'nvarchar': 'categorical',
        'bool': 'categorical',
        'boolean': 'categorical',
        'bit': 'categorical',
        'date': 'date',
        'datetime': 'datetime',
        'timestamp': 'datetime',
        # 'time': 'date',
        'int': 'numeric',
        'bigint': 'numeric',
        'smallint': 'numeric',
        'tinyint': 'numeric',
        'integer': 'numeric',
        'float': 'numeric',
        'double': 'numeric',
        'decimal': 'numeric',
        'dec': 'numeric',
        'long': 'numeric',
        'numeric': 'numeric',
        'int64': 'numeric',
        'float64': 'numeric',
        'real': 'numeric'
    }
    return type_dict.get(column_type.lower().split('(')[0], 'unsupported')

def _create_semantic_model(atconn: Connection, dbconn: SQLConnection, table_name: str, project_dict: dict, cube_id: str, dataset_id: str, columns: list):
    """Mutates the provided project_dict to add a semantic layer. NOTE: This does not update the project! Calling methods must still update and publish the project using the resulting project_dict. 

    Args:
        atconn (Connection): AtScale connection
        dbconn (SQLConnection): DB connection
        table_name (str): the name of the table to create a semantic table for
        project_dict (dict): the project dictionary (generally sparse result of creating a new project and adding a dataset)
        cube_id (str): the id for the cube (generally sparse result of creating a new project)
        dataset_id (str): the id for the dataset associated with the table_name for which we will create a semantic layer
        columns (list[tuple]): columns of the table associated with table_name and dataset_id as AtScale sees them, generally with a name and type for each
    """
    for column in columns:
        column_name = column[0]
        column_type = _get_column_type_category(column[1])

        if column_type == 'unsupported':
            logger.warning(f"column {column_name} is of unsupported type {column[1].lower().split('(')[0]}, skipping the modeling of this column")
            continue

        # could pile on the various numeric types, not sure how AtScale sees them all, so far I've seen "Decimal" a lot.
        elif column_type == 'numeric':
            # Note that calculated columns pulling out parts of dates will show up as Decimal data type also.
            feature_utils._create_aggregate_feature_local(
                project_dict=project_dict, cube_id=cube_id, dataset_id=dataset_id, column_name=column_name, name = column_name+'_SUM', aggregation_type=enums.Aggs.SUM)

        # this does a string comparison to see if this column type is a DateTime
        elif column_type in ('date', 'datetime'):
            # Add a dimension for the date column
            try:#determine_time_levels depends on count(distinct(column_name)) sql working. If the db errors out, then we just skip
                #if the column_type_category is time then start level should be hours
                
                # time is not currently supported by atscale, we need to look into this with the modeler team  
                # if column[1].lower().split('(')[0] == 'time':    
                #     time_levels = time_utils.determine_time_levels(
                #         dbconn=dbconn, table_name=table_name, column=column_name, start_level= enums.TimeLevels.Hour)
                # else:
                end_level = max([e.index for e in enums.TimeLevels])
                if column_type == 'date':
                    end_level = enums.TimeLevels.Day

                time_levels = time_utils.determine_time_levels(
                    dbconn=dbconn, table_name=table_name, column=column_name, end_level= end_level)
            except Exception as e:
                logger.warning(f"Unable to determine TimeLevels in create_semantic_model for column {column} and db type {dbconn.platform_type}. The error was{e}")
                #skip the rest and go to the next column in the loop
                continue 
            dimension_utils.create_time_dimension_for_column(
                atconn=atconn, project_dict=project_dict, cube_id=cube_id, dataset_id=dataset_id, column_name=column_name, time_levels=time_levels)
        
        #only other option is if it is categorical
        else:
            dimension_utils.create_categorical_dimension_for_column(
                project_dict=project_dict, cube_id=cube_id, dataset_id=dataset_id, column_name=column_name)


    # The default data_model object when creating a project and writing a dataframe only has a data-set-ref. If we added dimensions above,
    # then we need to add some other dict elements to the data_model. I'm not actually sure how these are used. Just going with some defaults here
    data_model_dict = project_parser.get_cube(
        project_dict=project_dict, id=cube_id)
    data_model_dict.setdefault(
        'properties', templates.create_data_model_properties_dict_default())
    data_model_dict.setdefault(
        'actions', templates.create_data_model_actions_dict_default())
    # this being empty seems weird since we have calculated columns, but maybe this refers to calculated measures?
    data_model_dict.setdefault('calculated-members', {})
    data_model_dict.setdefault('aggregates', {})
    
def _get_fact_dataset_names(data_model: DataModel, project_dict: Dict) -> List[str]:
    """Gets the name of all fact datasets currently utilized by the DataModel and returns as a list.

    Args:
        data_model (DataModel): the datamodel to get datasets of interest from
        project_dict (Dict): the project_dict to extract dataset metadata from

    Returns:
        List[str]: list of fact dataset names
    """
    all_datasets = data_model_parser.get_project_datasets_referenced_by_cube(
        project_dict, _get_model_dict(data_model= data_model, project_dict= project_dict)[0])
    if len(all_datasets) > 0:
        return [dataset.get('name') for dataset in all_datasets]
    return all_datasets

def _get_dimension_dataset_names(data_model: DataModel, project_dict: Dict) -> List[str]:
    """Gets the name of all fact datasets currently utilized by the DataModel and returns as a list.

    Args:
        data_model (DataModel): the datamodel to get datasets of interest from
        project_dict (Dict): the project_dict to extract dataset metadata from

    Returns:
        List[str]: list of dimension dataset names
    """
    hierarchies = data_model.get_hierarchies().keys()
    participating_datasets = []
    for dimension in project_dict.get('dimensions', {}).get('dimension', []):
        for hierarchy in dimension.get('hierarchy', []):
            if hierarchy.get('name') in hierarchies:
                for participating_dataset in dimension.get('participating-datasets', []):
                    participating_datasets.append(participating_dataset)
                break
    all_datasets = []
    for dataset in project_parser.get_datasets(project_dict):
        if dataset.get('id') in participating_datasets:
            all_datasets.append(dataset.get('name'))
    return all_datasets

def _get_model_dict(data_model: DataModel, project_dict: Dict) -> Tuple[dict, dict]:
    """Returns one or two dictionaries associated with this data_model
    
    Args:
        data_model (DataModel): the datamodel to get information from
        project_dict (Dict): the project_dict to extract the datamodel dict from

    Returns:                     
        Tuple[dict, dict]: returns the cube and perspective respectively, where perspective may be None
    """
    cube_dict = None
    perspective_dict = None
# 
    if data_model.is_perspective():
        perspective_dict = project_parser.get_data_model(
            project_dict, data_model.id)
        cube_dict = project_parser.get_data_model(
            project_dict, data_model.cube_id)
    else:
        cube_dict = project_parser.get_data_model(project_dict, data_model.id)
    return cube_dict, perspective_dict

def _fact_dataset_exists(data_model: DataModel, project_dict: Dict, dataset_name: str) -> bool:
    """Returns whether a given dataset_name exists in the data model, case-sensitive.

    Args:
        data_model (DataModel): The DataModel object to search through
        project_dict (Dict): the project dict to look for the dataset in
        dataset_name (str): the name of the dataset to try and find

    Returns:
        bool: true if name found, else false.
    """
    allCubeDatasets = _get_fact_dataset_names(data_model, project_dict)
    matchFoundList = [
        dset for dset in allCubeDatasets if dset == dataset_name]

    return len(matchFoundList) > 0

def _dimension_dataset_exists(data_model: DataModel, project_dict: Dict, dataset_name: str) -> bool:
    """Returns whether a given dataset_name exists in the data model, case-sensitive.

    Args:
        data_model (DataModel): The DataModel object to search through
        project_dict (Dict): the project dict to look for the dataset in
        dataset_name (str): the name of the dataset to try and find

    Returns:
        bool: true if name found, else false.
    """
    dimension_datasets = _get_dimension_dataset_names(data_model, project_dict)
    matchFoundList = [
        dset for dset in dimension_datasets if dset == dataset_name]

    return len(matchFoundList) > 0

def _get_column_names(project_dict: Dict, dataset_name: str) -> List[str]:
    """Gets a list of all currently visible columns in a given dataset, case-sensitive.

    Args:
        project_dict (Dict): the project dict to look for the columns in
        dataset_name (str): the name of the dataset to get columns from, case-sensitive.

    Returns:
        List[str]: the column names in the given dataset
    """

    dataset_of_int = project_parser.get_dataset_from_datasets_by_name(project_parser.get_datasets(
        project_dict= project_dict), dataset_name)

    physical_list = dataset_of_int.get('physical')
    if physical_list is None:
        return []

    column_list = physical_list.get('columns', [])
    
    ret_list = []
    for map_col in physical_list.get('map-column', []):
        ret_list += map_col.get('columns', {}).get('columns', [])

    ret_list += column_list
    return [columnVal.get('name') for columnVal in ret_list]

def _column_exists(project_dict: Dict, dataset_name: str, column_name: str) -> bool:
    """Checks if the given column name exists in the dataset.

    Args:
        project_dict (Dict): the project dict to look for the column in
        dataset_name (str): the name of the dataset we pull the columns from, case-sensitive.
        column_name (str): the name of the column to check, case-sensitive

    Returns:
        bool: true if name found, else false.
    """
    all_column_names = _get_column_names(project_dict, dataset_name)
    match_found_list = [
        col_name for col_name in all_column_names if col_name == column_name]

    return len(match_found_list) > 0

def _perspective_check(data_model: DataModel, error_msg: str = None):
    """Checks if the data_model provided is a perspective and throws an error if so.

    Args:
        data_model (DataModel): The DataModel to check
        error_msg (str, optional): Custom error string. Defaults to None to throw write error.
    """
    if error_msg is None:
        error_msg = 'Write operations are not supported for perspectives.'
    
    if data_model.is_perspective():
        raise atscale_errors.UserError(error_msg)

def _add_related_hierarchies(data_model: DataModel, hierarchy_list: List[str], hierarchies_to_check: List[str] = None) -> None:
    """Recursively adds hierarchies to hierarchy_list if they are related to a hierarchy in hierarchies_to_check.

    Args:
        data_model (DataModel): The DataModel to check
        hierarchy_list (List[str]): The list of hierarchies to add to.
        hierarchies_to_check (List[str], optional): The list of hierarchies to look  for relationships with. If None will use hierarchy_list.
    
    Returns:
        None
    """
    if hierarchies_to_check is None:
        hierarchies_to_check = hierarchy_list
    project_dict = data_model.project._get_dict()
    cube_dict = _get_model_dict(data_model, project_dict= project_dict)[0]
    hierarchy_relationship_dict = {}
    # build a dictionary of the hierarchy names and their levels and relationships
    for dimension in project_dict.get('dimensions', {}).get('dimension', []) + cube_dict.get('dimensions', {}).get('dimension', []):
            for hierarchy in dimension.get('hierarchy', []):
                hierarchy_name = hierarchy.get('name')
                hierarchy_relationship_dict[hierarchy_name] = {'primary_attribute_keys':[],'relationship_keys':[]}
                for level in hierarchy.get('level', []):
                    hierarchy_relationship_dict[hierarchy_name]['primary_attribute_keys'].append(level.get('primary-attribute'))
                    for keyed_attribute_ref in level.get('keyed-attribute-ref', []):
                        hierarchy_relationship_dict[hierarchy_name]['relationship_keys'].append(keyed_attribute_ref.get('attribute-id'))
    # call the recursive helper to use the dict to add related hierarchies so we don't have to build it each time
    _add_related_hierarchies_helper(hierarchy_list, hierarchies_to_check, hierarchy_relationship_dict)

def _add_related_hierarchies_helper(hierarchy_list: List[str], hierarchies_to_check: List[str], hierarchy_relationship_dict: Dict) -> None:
    """Recursively adds hierarchies to hierarchy_list if they are related to a hierarchy in hierarchies_to_check.

    Args:
        hierarchy_list (List[str]): The list of hierarchies to add to.
        hierarchies_to_check (List[str]): The list of hierarchies to look  for relationships with.
        hierarchy_relationship_dict (Dict): A dictionary with hierarchy names as keys that contains their attributes and relationships.
    
    Returns:
        None
    """
    new_hierarchies_to_check = []
    for hierarchy in hierarchies_to_check:
        # the relationship info is only stored in one hierarchy so we need to check both ways
        for key in hierarchy_relationship_dict[hierarchy]['relationship_keys']:
            for hier in hierarchy_relationship_dict.keys():
                if hier not in hierarchy_list and key in hierarchy_relationship_dict[hier]['primary_attribute_keys']:
                    hierarchy_list.append(hier)
                    new_hierarchies_to_check.append(hier)
        for key in hierarchy_relationship_dict[hierarchy]['primary_attribute_keys']:
            for hier in hierarchy_relationship_dict.keys():
                if hier not in hierarchy_list and key in hierarchy_relationship_dict[hier]['relationship_keys']:
                    hierarchy_list.append(hier)
                    new_hierarchies_to_check.append(hier)
    # if we added new hierarchies we recursively call the function to see if there are other hierarchies we need to bring in connected to those new ones
    if len(new_hierarchies_to_check) > 0:
        _add_related_hierarchies_helper(hierarchy_list, new_hierarchies_to_check, hierarchy_relationship_dict)

def _validate_mdx_syntax(data_model: DataModel, expression: str):
    url = endpoints._endpoint_mdx_syntax_validation(data_model.project.atconn)
    data = {'formula':expression}
    response = data_model.project.atconn._submit_request(request_type=enums.RequestType.POST, url=url, data=json.dumps(data))
    resp = json.loads(response.content)['response']
    if not resp['isSuccess']:
        raise atscale_errors.UserError(resp['errorMsg'])
