import logging
import uuid

from atscale.parsers import project_parser
from atscale import atscale_errors
from atscale.utils import project_utils, request_utils

logger = logging.getLogger(__name__)


def check_features(features: list, check_list: list, errmsg: str = None):
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


def create_dataset_ref(dataset_id, key_refs, attribute_refs):
    dataset = {
        'id': dataset_id,
        'properties': {
            'allow-aggregates': True,
            'create-hinted-aggregate': False,
            'aggregate-destinations': None
        },
        'logical': {
            'key-ref': key_refs,
            'attribute-ref': attribute_refs
        }}
    return dataset


def create_dataset_relationship(atconn, project_dict, cube_id, database, schema, table_name, join_features, join_columns=None, roleplay_features=None):
    warehouse_id = project_utils.get_project_warehouse(project_dict)
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

    # This was commented out in atscale_comments.py so just leaving that way here
    # check_multiple_features(join_features, self.list_all_categorical_features(),
    #                              errmsg='Make sure all items in join_features are categorical features')

    url = f'{atconn._warehouse_endpoint()}/conn/{warehouse_id}/tables/cacheRefresh'
    request_utils.post_request(url=url, headers=atconn._generate_headers())

    # we'll use table_columns potentially for creating a dataset below and then more logic after that
    table_columns = atconn.get_table_columns(warehouse_id=warehouse_id,
                                             table_name=table_name,
                                             database=database,
                                             schema=schema)

    # there was a check as to whether the datasets element was null which set it to an empty list. I'm not sure if that would
    # ever be possible. If so, I imagine project_datasets would have to be null, and then verify_connection would fail. If we
    # want to support this, then we'd have to change verify to not check project_data set values. I rearranged the logic a lot.
    # Figured that was safe to pull out into an independent check here.
    if project_dict['datasets']['data-set'] is None:
        project_dict['datasets']['data-set'] = []

    # look for a dataset that may already have the table_name for the table we're trying to join to the cube (meaning the table
    # already exists and we're just replacing it or appending it)
    dataset_id = project_parser.find_dataset_with_table(
        project_datasets, table_name)

    if not dataset_id:  # then we have to create a project_dataset
        # the prior code assumed a schema but checked if database was None prior to setting
        project_dataset, dataset_id = project_utils.create_dataset(
            table_name, warehouse_id, table_columns, database, schema)
        # and we'll add the newly minted dataset to the project_dict
        project_dict['datasets']['data-set'].append(project_dataset)

    key_refs = []
    attribute_refs = []

    joins = tuple(zip(join_features, join_columns, roleplay_features))
    cube_dict = project_parser.get_cube(project_dict, cube_id)

    for join_feature, join_column, roleplay_feature in joins:
        # Questions :
        # Why are we making a list for each join feature, column, and roleplay feature?
        # Cols is a list and we set it on key_ref - can that literally be more than on column? Why is it a list? If it is a list, why is the key not cols instead of col?
        if type(join_column) != list:
            # won't this always be called? we didn't specify to provide a lists of lists where each element is a single item.
            join_column = [join_column]

        # looks in the project for an attribute that matches the join feature. If one is found,
        # it determines if user specified it as a roleplay feature. If they did, it looks for the name
        # at the current location to see if it matches the name provided by the user for the roleplay feature
        # and if that is not found, it appends the current name in place, to the provided roleplay  feature,
        # and constructs the json around it, like ref_id, and sets it up to reference the dimension id
        dimension = None
        if 'attributes' in project_dict and 'keyed-attribute' in project_dict['attributes']:
            dimension = [x for x in project_dict['attributes']
                         ['keyed-attribute'] if x['name'] == join_feature]
            if dimension:
                ref = dimension[0]['key-ref']
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
                            'attribute-id': dimension[0]['id'],
                            'ref-id': ref_id,
                            'ref-naming': roleplay_feature
                        }
                    }
                    key_ref['ref-path'] = ref_path
                key_refs.append(key_ref)

        # if the join features was not found as a dimension in project_json above, look in the cube.
        # I'm a little confused by passing in cols because cols is a list
        if not dimension:
            if 'attributes' in cube_dict and 'keyed-attribute' in cube_dict['attributes']:
                dimension = [x for x in cube_dict['attributes']
                             ['keyed-attribute'] if x['name'] == join_feature]
                if dimension:
                    ref = dimension[0]['key-ref']
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
                                'attribute-id': dimension[0]['id'],
                                'ref-id': ref_id,
                                'ref-naming': roleplay_feature
                            }
                        }
                        key_ref['ref-path'] = ref_path
                    key_refs.append(key_ref)
                    uid = dimension[0]['id']
                    attr = {
                        'id': uid,
                        'complete': 'partial',
                        'column': join_column
                    }
                    attribute_refs.append(attr)
    found = False
    if 'data-set-ref' in cube_dict['data-sets']:
        for ds_ref in cube_dict['data-sets']['data-set-ref']:
            if ds_ref['id'] == dataset_id:
                found = True
                if 'key-ref' in ds_ref['logical']:
                    ds_ref['logical']['key-ref'] = ds_ref['logical']['key-ref'] + key_refs
                else:
                    ds_ref['logical']['key-ref'] = key_refs
                if 'attribute-ref' in ds_ref['logical']:
                    ds_ref['logical']['attribute-ref'] = ds_ref['logical']['attribute-ref'] + attribute_refs
                else:
                    ds_ref['logical']['attribute-ref'] = attribute_refs
    else:
        # It's unlikley the cube would have no element at all for a dataset ref, but just in case, this is in here
        cube_dict['data-set']['data-set-ref'] = []

    # If we had to create a dataset for the project to point at the new table, then we need to ensure there is also one in the cube referencing it.
    # This check previously referred back to "found" which was based on the project data set being there, but this is really about whether we
    # find it in the cube, which is in the logic immediately above, so I'll do the boolean there instead.
    if not found:
        data_set_ref = create_dataset_ref(dataset_id, key_refs, attribute_refs)
        cube_dict['data-sets']['data-set-ref'].append(data_set_ref)

    return project_dict
