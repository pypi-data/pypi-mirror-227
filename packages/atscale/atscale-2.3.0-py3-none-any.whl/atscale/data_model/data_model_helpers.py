import copy
import logging
import pandas as pd
from typing import List, Set, Union
from atscale.base.enums import Measure, Level, Hierarchy, FeatureType
from atscale.db.sql_connection import SQLConnection
from atscale.utils.dmv_utils import get_dmv_data
from atscale.utils import db_utils, model_utils
from atscale.errors import atscale_errors
from atscale.parsers import project_parser


def _get_unpublished_features(project_dict, data_model_name, feature_list: List[str] = None, folder_list: List[str] = None,
                              feature_type: FeatureType = FeatureType.ALL) -> dict:
    """Gets the feature names and metadata for each feature in the published DataModel.

        Args:
            project_dict (dict): the metadata of the project to extract
            data_model_name (str): the name of the data_model of interest
            feature_list (List[str], optional): A list of features to return. Defaults to None to return all.
            folder_list (List[str], optional): A list of folders to filter by. Defaults to None to ignore folder.
            feature_type (FeatureType, optional): The type of features to filter by. Options
                include FeatureType.ALL, FeatureType.CATEGORICAL, or FeatureType.NUMERIC. Defaults to ALL.

        Returns:
            dict: A dictionary of dictionaries where the feature names are the keys in the outer dictionary
                  while the inner keys break down metadata of the features.
        """
    start_dict = {}
    # metrical attributes and levels
    start_dict.update(_parse_roleplay_features(
        data_model_name, project_dict))
    if feature_type in [FeatureType.NUMERIC, FeatureType.ALL]:
        start_dict.update(_parse_aggregate_features(
            data_model_name, project_dict))
        start_dict.update(_parse_calculated_features(
            data_model_name, project_dict))
    if feature_type in [FeatureType.CATEGORICAL, FeatureType.ALL]:
        start_dict.update(_parse_denormalized_categorical_features(
            data_model_name, project_dict))

    feature_list = [feature_list] if isinstance(
        feature_list, str) else feature_list
    folder_list = [folder_list] if isinstance(
        folder_list, str) else folder_list

    ret_dict = copy.deepcopy(start_dict)
    for i in start_dict:
        if feature_list is not None:
            if i not in feature_list:
                del ret_dict[i]
        if folder_list is not None:
            if all(folder_val not in folder_list for folder_val in ret_dict[i]['folder']):
                del ret_dict[i]
        if feature_type != FeatureType.ALL:
            if ret_dict[i]['feature_type'] != feature_type.name_val:
                del ret_dict[i]
    return ret_dict


def _check_joins(project_dict: dict,
                                cube_id: str,
                                join_features: List[str],
                                join_columns: List[Union[str, List[str]]],
                                column_set: set,
                                roleplay_features: List[str] = None,
                                dbconn: SQLConnection = None,
                                df: pd.DataFrame = None,
                                key_dict=None,
                                feature_dict=None,
                                spark_input: bool = False):
    """ Checks that the join features and columns are valid and either errors or returns join_features, join_columns, and df.
    Args:
        project_dict (dict): the metadata of the project to validate against
        cube_id (str): the id of the cube to validate against
        join_features (List[str]): the list of features to join on
        join_columns (List[str]): the list of columns to join on
        column_set (set): the set of columns in the table or dataframe
        roleplay_features (List[str], optional): the list of roleplay features to join on. 
            Defaults to None to be set as a list of '' for each join features.
        dbconn (SQLConnection, optional): the connection to the database, used for querying columns as defined in atscale 
        in case df is passsed and needs value columns to be mapped to query columns. Defaults to None.
        df (pd.DataFrame, optional): the dataframe to validated before writing to db and model. Defaults to None.
        key_dict (dict, optional): The key dict returned by calling _get_feature_keys for the join_features. 
            Defaults to None to retrieve it.
        feature_dict (dict, optional): The feature dict returned by calling _get_unpublished_features for the join_features. 
            Defaults to None to call the method and retrieve it.
        spark_input (bool, optional): if the input df is spark or pandas, defaults to False.
        """
    column_set: Set[str] = set(column_set)
    if join_features is None:
        join_features = []
    if join_columns is None:
        join_columns = join_features
    elif len(join_features) != len(join_columns):
        raise atscale_errors.UserError(f'join_features and join_columns must be equal lengths. join_features is'
                                       f' length {len(join_features)} while join_columns is length {len(join_columns)}')
    # copy so if we make a feature a list, or change its name, it doesn't change the original
    join_columns = join_columns.copy()
    if roleplay_features is None:
        roleplay_features = ['' for feature in join_features]
    elif len(join_features) != len(roleplay_features):
        raise atscale_errors.UserError(f'join_features and roleplay_features lengths must match. '
                                       f'join_features is length {len(join_features)} '
                                       f'while roleplay_features is length {len(roleplay_features)}')

    if feature_dict is None:
        model_name = project_parser.get_cube(project_dict=project_dict,
                                             id=cube_id)["name"]
        feature_dict = _get_unpublished_features(data_model_name=model_name,
                                                 project_dict=project_dict)
    # need to get a set of features that includes base names of roleplayed features
    levels = {}
    # also need the set of only base names of levels (not secondary attributes either)
    base_names = {}
    for feat, info in feature_dict.items():
        if info['feature_type'] == FeatureType.CATEGORICAL.name_val:
            if feat != info.get('base_name', feat):  # roleplayed
                base_names[info['base_name']] = info
            secondary_attribute = (
                feat == info['hierarchy'][0] and info.get('base_name', feat) != info.get('base_hierarchy', [''])[0])
            if not secondary_attribute:
                levels[info.get('base_name', feat)] = info
            # if there are more than one roleplay on the level, it will hold the info of just one
    feature_dict.update(base_names)

    features_not_in_model = []
    non_level_features = []
    for f in join_features:
        if f not in feature_dict:
            features_not_in_model.append(f)
        elif f not in levels:
            non_level_features.append(f)
    err_msg = ""
    if features_not_in_model:
        err_msg += f'The following features in join_features do not exist in the data model: {features_not_in_model}\n'
    if non_level_features:
        err_msg += f'Joins must be made exclusively to hierarchy levels, the following items in ' \
                   f'join_features are not levels of a hierarchy: {non_level_features}.'
    if err_msg:
        raise atscale_errors.UserError(err_msg)

    # Verify the join_columns (which may be join_features now) are in the dataframe columns.
    key_dict = project_parser._get_feature_keys(
        project_dict, cube_id, join_features) if key_dict is None else key_dict
    missing_join_columns = []
    
    for i, column in enumerate(join_columns):
        if type(column) is not list:
            column = [column]
            join_columns[i] = column
        for col in column:
            if col not in column_set:
                missing_join_columns.append(col)
    if missing_join_columns:
        raise atscale_errors.UserError(
            f'The given join_columns {missing_join_columns} do not exist in the column set {list(column_set)}.'
        )

    # users are going to know the feature names associated with values, but the feature names don't always map to
    # the feature keys. So if they pass column name that is victim to this, try and adjust it to match the key.
    for i, (join_feature, join_column) in enumerate(zip(join_features, join_columns)):
        key_cols: List[str] = key_dict[join_feature]["key_cols"]
        value_col: str = key_dict[join_feature]["value_col"]
        # alert the user to a missed multi-key
        if len(join_column) != len(key_cols):
            raise atscale_errors.UserError(
                f'Relationship for feature: "{join_feature}" '
                f'requires {len(key_cols)} key{"s" if len(key_cols) > 1 else ""}: {key_cols} '
                f'but received {len(join_column)}: {join_column}')
        if dbconn is not None and df is not None:
            # if the column is from an atscale query and the value returned is not the join key
            # then we assume that the join_column is an alias for the value column when it should be the key column
            if len(key_cols) == 1 and key_cols[0] != value_col and join_column[0] == join_feature:
                df_key: pd.DataFrame = db_utils._get_key_cols(
                    dbconn, key_dict[join_feature])
                if df_key is not None:
                    if join_column[0] != value_col:
                        df_key.rename(columns={
                            value_col: join_column[0]}, inplace=True)  # rename df_key value column to given join_column
                    if spark_input:
                        spark_session = df.sparkSession
                        df_key = spark_session.createDataFrame(df_key)
                        df = df.join(df_key, how='left', on=join_column[0])
                    else:
                        df = pd.merge(df, df_key, how='left', on=join_column[0])
                    # merge on given join_column name
                    
                    join_columns[i] = [key_cols[0]]
    return join_features, join_columns, roleplay_features, df


def _prep_join_columns_for_join(join_columns: List[List[str]],
                                 atscale_columns: List[str]) -> List[List[str]]:
    """Prepares the join columns for the join by replacing any column names that are aliases with the actual column name and making each item a list.

    Args:
        join_columns: The columns to join on.
        atscale_columns: The columns as they appear in the atscale dataset.

    Returns:
        The join columns with any aliases replaced with the actual column names.
    """
    if join_columns is None:
        return join_columns
    else:
        join_columns = join_columns.copy()  # always copy before mutating, the user could've used the param twice
    atscale_columns = set(atscale_columns)
    for i, joins in enumerate(join_columns):
        if type(joins) is not list:
            join_columns[i] = [joins]
            joins = [joins]
        for j, col in enumerate(joins):
            if col in atscale_columns:
                continue
            elif col.upper() in atscale_columns:
                join_columns[i][j] = col.upper()
            elif col.lower() in atscale_columns:
                join_columns[i][j] = col.lower()
    return join_columns


def _parse_roleplay_features(data_model_name, project_dict):
    """ Pulls metadata on roleplayed features

    Args:
        data_model_name (str): the name of the data_model of interest
        project_dict (dict): the metadata of the project to extract

    Returns:
        Dict[Dict]: a dict of dicts of the form 'query_name':{metadata} 
    """
    info_dict = {}

    if 'attributes' not in project_dict or 'keyed-attribute' not in project_dict['attributes']:
        return {}

    for i in project_dict['attributes']['keyed-attribute']:
        info_dict[i['id']] = i

    # deal with metrical secondary attributes
    if 'attribute' in project_dict['attributes']:
        for i in project_dict['attributes']['attribute']:
            info_dict[i['id']] = i

    roleplay_refs = {}
    cube = [x for x in project_dict['cubes']['cube']
            if x['name'] == data_model_name][0]

    for dataset in cube['data-sets']['data-set-ref']:
        if 'key-ref' in dataset['logical']:
            for key in dataset['logical']['key-ref']:
                if key['complete'] == 'false':
                    if 'ref-path' in key:
                        val = (key['ref-path']['new-ref']['ref-naming'], key['ref-path']['new-ref']['ref-id'])
                    else:
                        val = ('{0}','')
                    roleplay_refs.setdefault(key['id'], [])
                    roleplay_refs[key['id']].append(val)

    # need this to handle snowflake dimensions
    for dimension in project_dict['dimensions']['dimension']:
        for hierarchy in dimension['hierarchy']:
            for level in hierarchy['level']:
                if 'properties' in level and level['properties'].get('visible', True):
                    if 'keyed-attribute-ref' in level:
                        for key in level['keyed-attribute-ref']:
                            # I don't think this can be hit
                            if 'ref-path' in key['properties']:
                                val = (key['properties']['ref-path']['new-ref']['ref-naming'], key['properties']['ref-path']['new-ref']['ref-id'])
                            else:
                                val = ('{0}','')
                            roleplay_refs.setdefault(key['attribute-id'], [])
                            roleplay_refs[key['attribute-id']].append(val)
                    #added in 'attribute-ref to deal with metrical secondary attributes 
                    if 'attribute-ref' in level:
                        for key in level['attribute-ref']:
                            roleplay_refs.setdefault(key['attribute-id'], [])
                            roleplay_refs[key['attribute-id']].append(('{0}',''))

    roleplay_ids = {}
    ref_ids = {}
    for key_ref in project_dict['attributes']['keyed-attribute']:
        if key_ref.get('key-ref', None) and key_ref['key-ref'] in roleplay_refs:
            roleplay_ids[key_ref['id']] = roleplay_refs[key_ref['key-ref']]
        # this seems necessary for snowflake dimensions
        elif key_ref.get('id', None) and key_ref['id'] in roleplay_refs:
            roleplay_ids[key_ref['id']] = roleplay_refs[key_ref['id']]
        ref_ids[key_ref['id']] = key_ref

    # for metrical attributes
    if 'attribute' in project_dict['attributes']:
        for key_ref in project_dict['attributes']['attribute']:
            if key_ref.get('key-ref', None) and key_ref['key-ref'] in roleplay_refs:
                roleplay_ids[key_ref['id']] = roleplay_refs[key_ref['key-ref']]
            # this seems necessary for snowflake dimensions
            elif key_ref.get('id', None) and key_ref['id'] in roleplay_refs:
                roleplay_ids[key_ref['id']] = roleplay_refs[key_ref['id']]
            key_ref['level-type'] = 'Aggregate'
            key_ref['feature-type'] = 'Numeric'
            ref_ids[key_ref['id']] = key_ref

    dim_to_id_dict = {}

    for dimension in project_dict['dimensions']['dimension']:
        for hierarchy in dimension['hierarchy']:
            if 'folder' in hierarchy['properties']:
                this_folder = hierarchy['properties']['folder']
            else:
                this_folder = ''
            roleplays = set()
            # reversed so that we only apply role playing above the leaf
            for level in reversed(hierarchy['level']):
                if level['primary-attribute'] in roleplay_ids:
                    roleplays.add(level['primary-attribute'])
                for roleplay in roleplays:
                    # This visiblity was seemingly ignored, so we  can remove it
                    # if ref_ids[level['primary-attribute']]['properties'].get('visible', False):
                    if level.get('properties', {}).get('visible', True):
                        for (role, ref_id) in roleplay_ids[roleplay]:  
                            roleplaying_dict = {}
                            if level.get('properties', {}).get('level-type', []):
                                roleplaying_dict['level_type'] = level['properties']['level-type']
                            else:
                                roleplaying_dict['level_type'] = 'Standard'
                            roleplaying_dict['id'] = ref_ids[level['primary-attribute']]['id']
                            rp_name = role.replace(
                                '{0}', ref_ids[level['primary-attribute']]['name'])
                            roleplaying_dict['roleplay_expression'] = role
                            roleplaying_dict['roleplay_ref_id'] = ref_id
                            roleplaying_dict['roleplayed_name'] = rp_name
                            roleplaying_dict['folder'] = [this_folder]
                            roleplaying_dict['roleplayed_hierarchy'] = [
                                role.replace('{0}', hierarchy['name'])]
                            roleplaying_dict['roleplayed_dimension'] = role.replace(
                                '{0}', dimension['name'])
                            roleplaying_dict['roleplayed_caption'] = role.replace('{0}',
                                                                                  info_dict[roleplaying_dict['id']]['properties']['caption'])
                            roleplaying_dict['base_name'] = ref_ids[level['primary-attribute']]['name']
                            roleplaying_dict['base_hierarchy'] = [
                                hierarchy['name']]
                            roleplaying_dict['base_dimension'] = dimension['name']

                            # deal with multiple hierachies with same roleplay method
                            if rp_name in dim_to_id_dict:
                                for found_key, found_value in roleplaying_dict.items():
                                    current_val = dim_to_id_dict[rp_name].get(
                                        found_key, [])
                                    if type(current_val) == list and len(current_val) > 0:
                                        dim_to_id_dict[rp_name][found_key].extend(
                                            found_value)
                                    else:
                                        dim_to_id_dict[rp_name][found_key] = found_value
                            else:
                                dim_to_id_dict[rp_name] = roleplaying_dict

                    # these are the secondary attributes
                    if 'keyed-attribute-ref' in level:  # then find the base hierarchy (source for this rp'd one)
                        for attr in level['keyed-attribute-ref']:
                            # if it has a reference ID then it should be handled elsewhere as this is a join
                            ref_id_check = attr.get('ref-id', False)
                            if not ref_id_check and ref_ids[attr['attribute-id']]['properties'].get('visible', False):
                                for (role, ref_id) in roleplay_ids[roleplay]:
                                    roleplaying_dict = {}
                                    roleplaying_dict['id'] = ref_ids[attr['attribute-id']]['id']
                                    roleplaying_dict['roleplayed_name'] = role.replace('{0}',
                                                                                       ref_ids[attr['attribute-id']]['name'])
                                    if 'folder' in ref_ids[attr['attribute-id']]['properties']:
                                        roleplaying_dict['folder'] = [
                                            ref_ids[attr['attribute-id']]['properties']['folder']]
                                    else:
                                        roleplaying_dict['folder'] = [
                                            this_folder]
                                    roleplaying_dict['roleplay_expression'] = role
                                    roleplaying_dict['roleplay_ref_id'] = ref_id
                                    roleplaying_dict['roleplayed_hierarchy'] = [role.replace('{0}',
                                                                                            ref_ids[attr['attribute-id']]['name'])]
                                    roleplaying_dict['roleplayed_dimension'] = role.replace('{0}',
                                                                                            dimension['name'])
                                    roleplaying_dict['roleplayed_caption'] = role.replace('{0}',
                                                                                          info_dict[roleplaying_dict['id']]['properties']['caption'])
                                    roleplaying_dict['base_name'] = ref_ids[attr['attribute-id']]['name']
                                    roleplaying_dict['base_hierarchy'] = [
                                        hierarchy['name']]
                                    roleplaying_dict['base_dimension'] = dimension['name']

                                    dim_to_id_dict[roleplaying_dict['roleplayed_name']
                                                   ] = roleplaying_dict

                    # these are the metrical secondary attributes
                    if 'attribute-ref' in level:
                        for attr in level['attribute-ref']:
                            # if it has a reference ID then it should be handled elsewhere as this is a join
                            ref_id_check = attr.get('ref-id', False)
                            if not ref_id_check and ref_ids[attr['attribute-id']]['properties'].get('visible', False):
                                for (role, ref_id) in roleplay_ids[roleplay]:
                                    roleplaying_dict = {}
                                    roleplaying_dict['level_type'] = ref_ids[attr['attribute-id']
                                                                             ]['level-type']
                                    roleplaying_dict['feature_type'] = ref_ids[attr['attribute-id']
                                                                               ]['feature-type']
                                    roleplaying_dict['id'] = ref_ids[attr['attribute-id']]['id']
                                    roleplaying_dict['roleplay_expression'] = role
                                    roleplaying_dict['roleplay_ref_id'] = ref_id
                                    roleplaying_dict['roleplayed_name'] = role.replace('{0}',
                                                                                       ref_ids[attr['attribute-id']]['name'])
                                    roleplaying_dict['base_name'] = ref_ids[attr['attribute-id']]['name']

                                    if 'folder' in ref_ids[attr['attribute-id']]['properties']:
                                        roleplaying_dict['folder'] = [
                                            ref_ids[attr['attribute-id']]['properties']['folder']]
                                    else:
                                        roleplaying_dict['folder'] = [
                                            this_folder]
                                    roleplaying_dict['roleplayed_caption'] = role.replace('{0}',
                                                                                          info_dict[roleplaying_dict['id']]['properties']['caption'])
                                    dim_to_id_dict[roleplaying_dict['roleplayed_name']
                                                   ] = roleplaying_dict

    return_dict = {}
    for i in dim_to_id_dict:
        return_dict[i] = {}

    for i in dim_to_id_dict:
        return_dict[i]['caption'] = dim_to_id_dict[i].get(
            'roleplayed_caption', '')
        return_dict[i]['atscale_type'] = dim_to_id_dict[i].get(
            'level_type', 'Standard')
        try:
            return_dict[i]['description'] = info_dict[dim_to_id_dict[i]
                                                      ['id']]['properties']['description']
        except KeyError:
            return_dict[i]['description'] = ''
        return_dict[i]['hierarchy'] = dim_to_id_dict[i].get('roleplayed_hierarchy', [''])
        return_dict[i]['dimension'] = dim_to_id_dict[i].get('roleplayed_dimension', '')
        return_dict[i]['folder'] = dim_to_id_dict[i].get('folder', [''])
        return_dict[i]['feature_type'] = dim_to_id_dict[i].get('feature_type', 'Categorical')
        return_dict[i]['roleplay_expression'] =  dim_to_id_dict[i].get('roleplay_expression', '')
        if dim_to_id_dict[i].get('roleplay_ref_id', False):
            return_dict[i]['roleplay_ref_id'] = dim_to_id_dict[i]['roleplay_ref_id']
        return_dict[i]['base_name'] =  dim_to_id_dict[i].get('base_name', '')
        return_dict[i]['base_hierarchy'] =  dim_to_id_dict[i].get('base_hierarchy', '')
        return_dict[i]['base_dimension'] =  dim_to_id_dict[i].get('base_dimension', '')

        # deal with metricals
        if return_dict[i]['feature_type'] == 'Numeric':
            return_dict[i]['expression'] = ''
            del return_dict[i]['hierarchy']

    return return_dict


def _parse_aggregate_features(data_model_name, project_dict):
    """ Loads _feature_dict with information regarding aggregate features.

    Args:
        data_model_name (str): the name of the data_model of interest
        project_dict (dict): the metadata of the project to extract

    Returns:
        Dict[Dict]: a dict of dicts of the form 'query_name':{metadata}
    """
    return_dict = {}

    cube = [x for x in project_dict['cubes']['cube']
            if x['name'] == data_model_name][0]
    if 'attributes' not in cube or 'attribute' not in cube['attributes']:
        return {}  # Meaning no features have been added yet

    feature_info = [y for y in [x for x in cube['attributes']['attribute']]]

    for i in feature_info:
        return_dict[i['name']] = {}

    for i in feature_info:
        return_dict[i['name']]['caption'] = i.get(
            'properties', {}).get('caption', '')
        return_dict[i['name']]['atscale_type'] = 'Aggregate'
        return_dict[i['name']]['description'] = i.get(
            'properties', {}).get('description', '')
        return_dict[i['name']]['folder'] = [
            i.get('properties', {}).get('folder', '')]
        return_dict[i['name']]['feature_type'] = 'Numeric'
        return_dict[i['name']]['expression'] = ''

    return return_dict


def _parse_calculated_features(data_model_name, project_dict):
    """ Loads _feature_dict with information regarding calculated features.

    Args:
        data_model_name (str): the name of the data_model of interest
        project_dict (dict): the metadata of the project to extract

    Returns:
        Dict[Dict]: a dict of dicts of the form 'query_name':{metadata}
    """
    return_dict = {}

    if 'calculated-members' not in project_dict or 'calculated-member' not in project_dict[
            'calculated-members']:
        return {}  # Meaning no features have been added yet

    feature_info = [
        x for x in project_dict['calculated-members']['calculated-member']]

    for i in feature_info:
        return_dict[i['name']] = {}

    for i in feature_info:
        return_dict[i['name']]['caption'] = i.get(
            'properties', {}).get('caption', '')
        return_dict[i['name']]['atscale_type'] = 'Calculated'
        return_dict[i['name']]['description'] = i.get(
            'properties', {}).get('description', '')
        return_dict[i['name']]['folder'] = [
            i.get('properties', {}).get('folder', '')]
        return_dict[i['name']]['feature_type'] = 'Numeric'
        return_dict[i['name']]['expression'] = i['expression']

    return return_dict


def _parse_denormalized_categorical_features(data_model_name, project_dict):
    """ Loads _feature_dict with information regarding denormalized categorical features.

    Args:
        data_model_name (str): the name of the data_model of interest
        project_dict (dict): the metadata of the project to extract

    Returns:
        Dict[Dict]: a dict of dicts of the form 'query_name':{metadata}
    """
    return_dict = {}

    cube = [x for x in project_dict['cubes']['cube']
            if x['name'] == data_model_name][0]
    if 'attributes' not in cube or 'keyed-attribute' not in cube['attributes']:
        return {}

    feature_info = [x for x in cube['attributes']['keyed-attribute']]

    folder_info = {}
    for dimension in cube['dimensions']['dimension']:
        for hierarchy in dimension['hierarchy']:
            hierarchy_name = hierarchy['name']
            if 'folder' in hierarchy['properties']:
                this_folder = hierarchy['properties']['folder']
            else:
                this_folder = ''
            for level in hierarchy['level']:
                if level['primary-attribute'] in folder_info:
                    folder_info[level['primary-attribute']
                                ]['folder'].append(this_folder)
                    folder_info[level['primary-attribute']
                                ]['hierarchy'].append(hierarchy_name)
                else:
                    folder_info[level['primary-attribute']] = {'folder': [this_folder],
                                                               'hierarchy': [hierarchy_name],
                                                               'dimension': dimension['name']}

    for i in feature_info:
        return_dict[i['name']] = {}

    for i in feature_info:
        return_dict[i['name']]['caption'] = i.get(
            'properties', {}).get('caption', '')
        return_dict[i['name']]['atscale_type'] = 'Standard'
        return_dict[i['name']]['description'] = i.get(
            'properties', {}).get('description', '')
        return_dict[i['name']]['hierarchy'] = folder_info.get(
            i['id'], {}).get('hierarchy', '')
        return_dict[i['name']]['dimension'] = folder_info.get(
            i['id'], {}).get('dimension', '')
        return_dict[i['name']]['folder'] = folder_info.get(
            i['id'], {}).get('folder', '')
        return_dict[i['name']]['feature_type'] = 'Categorical'

    return return_dict


def _get_published_features(data_model, feature_list: List[str] = None, folder_list: List[str] = None,
                            feature_type: FeatureType = FeatureType.ALL) -> dict:
    """Gets the feature names and metadata for each feature in the published DataModel.

    Args:
        data_model (DataModel): The published atscale data model to get the features of via dmv 
        feature_list (List[str], optional): A list of features to return. Defaults to None to return all.
        folder_list (List[str], optional): A list of folders to filter by. Defaults to None to ignore folder.
        feature_type (FeatureType, optional): The type of features to filter by. Options
            include FeatureType.ALL, FeatureType.CATEGORICAL, or FeatureType.NUMERIC. Defaults to ALL.

    Returns:
        dict: A dictionary of dictionaries where the feature names are the keys in the outer dictionary 
                while the inner keys are the following:
                'atscale_type'(value is a level-type, 'Aggregate', or 'Calculated'),
                'description', 'expression', caption, 'folder', 'data_type', and 'feature_type'(value is Numeric or Categorical).
    """
    level_filter_by = {}
    measure_filter_by = {}
    hier_filter_by = {}
    if feature_list:
        feature_list = [feature_list] if isinstance(
            feature_list, str) else feature_list
        level_filter_by[Level.name] = feature_list
        measure_filter_by[Measure.name] = feature_list
    if folder_list:
        folder_list = [folder_list] if isinstance(
            folder_list, str) else folder_list
        hier_filter_by[Hierarchy.folder] = folder_list
        measure_filter_by[Measure.folder] = folder_list

    feature_dict = {}

    if feature_type is FeatureType.ALL or feature_type is FeatureType.CATEGORICAL:
        hier_dict = get_dmv_data(model=data_model,
                                 fields=[Hierarchy.folder],
                                 filter_by=hier_filter_by)
        level_filter_by[Level.hierarchy] = list(hier_dict.keys())

        dimension_dict = get_dmv_data(
            model=data_model,
            fields=[Level.type, Level.description, Level.hierarchy,
                    Level.caption, Level.data_type],
            filter_by=level_filter_by
        )
        for name, info in dimension_dict.items():
            # if a level was duplicated we might have multiple hierarchies which could mean multiple folders
            folder = []
            if type(info[Level.hierarchy.name]) is list:
                for hierarchy_name in info[Level.hierarchy.name]:
                    if hier_dict.get(hierarchy_name):
                        folder.append(
                            hier_dict[hierarchy_name][Hierarchy.folder.name])
            else:
                folder.append(
                    hier_dict[info[Level.hierarchy.name]][Hierarchy.folder.name])
                info[Level.hierarchy.name] = [info[Level.hierarchy.name]]

            feature_dict[name] = {
                'caption': info[Level.caption.name],
                'atscale_type': info[Level.type.name],
                'data_type': info[Level.data_type.name],
                'description': info[Level.description.name],
                'hierarchy': info[Level.hierarchy.name],
                'folder': folder,
                'feature_type': 'Categorical'}
    if feature_type is FeatureType.ALL or feature_type is FeatureType.NUMERIC:
        catalog_licensed = data_model.project.atconn._validate_license(
            'data_catalog_api')
        query_fields = [Measure.type, Measure.description,
                        Measure.folder, Measure.caption, Measure.data_type]
        if catalog_licensed:
            query_fields.append(Measure.expression)
        measure_dict = get_dmv_data(
            model=data_model,
            fields=query_fields,
            filter_by=measure_filter_by
        )
        for name, info in measure_dict.items():
            feature_dict[name] = {
                'caption': info[Measure.caption.name],
                'atscale_type': info[Measure.type.name],
                'data_type': info[Measure.data_type.name],
                'description': info[Measure.description.name],
                'folder': [info[Measure.folder.name]],
                'feature_type': 'Numeric'}
            if catalog_licensed:
                feature_dict[name]['expression'] = info[Measure.expression.name]
            else:
                feature_dict[name]['expression'] = ''

    return feature_dict
