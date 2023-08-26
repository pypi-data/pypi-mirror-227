import copy
from typing import List
from atscale.base.enums import  Measure, Level, Hierarchy, FeatureType
from atscale.utils.dmv_utils import get_dmv_data


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
        start_dict.update(_parse_roleplay_features(data_model_name, project_dict))  # metrical attributes and levels
        if feature_type in [FeatureType.NUMERIC, FeatureType.ALL]:
            start_dict.update(_parse_aggregate_features(data_model_name, project_dict))
            start_dict.update(_parse_calculated_features(data_model_name, project_dict))
        if feature_type in [FeatureType.CATEGORICAL, FeatureType.ALL]:
            start_dict.update(_parse_denormalized_categorical_features(data_model_name, project_dict))

        feature_list = [feature_list] if isinstance(feature_list, str) else feature_list
        folder_list = [folder_list] if isinstance(folder_list, str) else folder_list

        ret_dict = copy.deepcopy(start_dict)
        for i in start_dict:
            if feature_list is not None:
                if i not in feature_list: del ret_dict[i]
            if folder_list is not None:
                if all(folder_val not in folder_list for folder_val in ret_dict[i]['folder']):
                    del ret_dict[i]
            if feature_type != FeatureType.ALL:
                if ret_dict[i]['feature_type'] != feature_type.name_val:
                    del ret_dict[i]
        return ret_dict

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

    #deal with metrical secondary attributes
    if 'attribute' in project_dict['attributes']:
        for i in project_dict['attributes']['attribute']:
            info_dict[i['id']] = i

    roleplay_refs = {}
    cube = [x for x in project_dict['cubes']['cube'] if x['name'] == data_model_name][0]

    for dataset in cube['data-sets']['data-set-ref']:
        if 'key-ref' in dataset['logical']:
            for key in dataset['logical']['key-ref']:
                if key['complete'] == 'false':
                    if 'ref-path' in key:
                        val = key['ref-path']['new-ref']['ref-naming']
                    else:
                        val = '{0}'
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
                            # if 'ref-path' in key['properties']:
                            #     val = key['properties']['ref-path']['new-ref']['ref-naming']
                            # else:
                            #     val = '{0}'
                            roleplay_refs.setdefault(key['attribute-id'], [])
                            roleplay_refs[key['attribute-id']].append('{0}')
                    #added in 'attribute-ref to deal with metrical secondary attributes 
                    if 'attribute-ref' in level:
                        for key in level['attribute-ref']:
                            roleplay_refs.setdefault(key['attribute-id'], [])
                            roleplay_refs[key['attribute-id']].append('{0}')

    roleplay_ids = {}
    ref_ids = {}
    for key_ref in project_dict['attributes']['keyed-attribute']:
        if key_ref.get('key-ref', None) and key_ref['key-ref'] in roleplay_refs:
            roleplay_ids[key_ref['id']] = roleplay_refs[key_ref['key-ref']]
        # this seems necessary for snowflake dimensions
        elif key_ref.get('id', None) and key_ref['id'] in roleplay_refs:
            roleplay_ids[key_ref['id']] = roleplay_refs[key_ref['id']]
        ref_ids[key_ref['id']] = key_ref

    #for metrical attributes
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
            #reversed so that we only apply role playing above the leaf
            for level in reversed(hierarchy['level']):
                if level['primary-attribute'] in roleplay_ids:
                    roleplays.add(level['primary-attribute'])
                for roleplay in roleplays:
                    # This visiblity was seemingly ignored, so we  can remove it
                    # if ref_ids[level['primary-attribute']]['properties'].get('visible', False):
                    if level.get('properties', {}).get('visible', True):
                        for role in roleplay_ids[roleplay]:  
                            roleplaying_dict = {}
                            if level.get('properties', {}).get('level-type', []):
                                roleplaying_dict['level_type'] = level['properties']['level-type']  
                            else: roleplaying_dict['level_type'] = 'Standard'
                            roleplaying_dict['id'] = ref_ids[level['primary-attribute']]['id']
                            rp_name =  role.replace('{0}', ref_ids[level['primary-attribute']]['name'])
                            roleplaying_dict['roleplay_expression'] = role
                            roleplaying_dict['roleplayed_name'] = rp_name
                            roleplaying_dict['folder'] = [this_folder]
                            roleplaying_dict['roleplayed_hierachy'] =  [role.replace('{0}', hierarchy['name'])]
                            roleplaying_dict['roleplayed_dimension'] = role.replace('{0}', dimension['name'])
                            roleplaying_dict['roleplayed_caption'] = role.replace('{0}',
                                                                info_dict[roleplaying_dict['id']]['properties']['caption'])
                            roleplaying_dict['base_name'] = ref_ids[level['primary-attribute']]['name']
                            roleplaying_dict['base_hierarchy'] = [hierarchy['name']]
                            roleplaying_dict['base_dimension'] = dimension['name']

                            #deal with multiple hierachies with same roleplay method
                            if rp_name in dim_to_id_dict:
                                for found_key, found_value in roleplaying_dict.items():
                                    current_val = dim_to_id_dict[rp_name].get(found_key, [])
                                    if type(current_val) == list and len(current_val) > 0:
                                        dim_to_id_dict[rp_name][found_key].extend(found_value)
                                    else:
                                        dim_to_id_dict[rp_name][found_key] = found_value
                            else:
                                dim_to_id_dict[rp_name] = roleplaying_dict

                    #these are the secondary attributes
                    if 'keyed-attribute-ref' in level:
                        for attr in level['keyed-attribute-ref']:
                            #if it has a reference ID then it should be handled elsewhere as this is a join
                            ref_id_check = attr.get('ref-id', False)
                            if not ref_id_check and ref_ids[attr['attribute-id']]['properties'].get('visible', False):
                                for role in roleplay_ids[roleplay]:
                                    roleplaying_dict = {}
                                    roleplaying_dict['id'] = ref_ids[attr['attribute-id']]['id']  
                                    roleplaying_dict['roleplayed_name'] = role.replace('{0}',
                                                                        ref_ids[attr['attribute-id']]['name'])
                                    if 'folder' in ref_ids[attr['attribute-id']]['properties']:
                                        roleplaying_dict['folder'] = [ref_ids[attr['attribute-id']]['properties']['folder']]
                                    else:
                                        roleplaying_dict['folder'] = [this_folder]
                                    roleplaying_dict['roleplay_expression'] = role
                                    roleplaying_dict['roleplayed_hierachy'] =[role.replace('{0}',
                                                                        ref_ids[attr['attribute-id']]['name'])]
                                    roleplaying_dict['roleplayed_dimension'] = role.replace('{0}',
                                                                                             dimension['name'])
                                    roleplaying_dict['roleplayed_caption'] = role.replace('{0}',
                                                                    info_dict[roleplaying_dict['id']]['properties']['caption'])
                                    roleplaying_dict['base_name'] = ref_ids[attr['attribute-id']]['name']
                                    roleplaying_dict['base_hierarchy'] = [hierarchy['name']]
                                    roleplaying_dict['base_dimension'] = dimension['name']

                                    dim_to_id_dict[roleplaying_dict['roleplayed_name']] = roleplaying_dict
                    
                    #these are the metrical secondary attributes
                    if 'attribute-ref' in level:
                        for attr in level['attribute-ref']:
                            #if it has a reference ID then it should be handled elsewhere as this is a join
                            ref_id_check = attr.get('ref-id', False)
                            if not ref_id_check and ref_ids[attr['attribute-id']]['properties'].get('visible', False):
                                for role in roleplay_ids[roleplay]:
                                    roleplaying_dict = {}
                                    roleplaying_dict['level_type'] = ref_ids[attr['attribute-id']]['level-type']
                                    roleplaying_dict['feature_type'] =  ref_ids[attr['attribute-id']]['feature-type']
                                    roleplaying_dict['id'] = ref_ids[attr['attribute-id']]['id']  
                                    roleplaying_dict['roleplay_expression'] = role
                                    roleplaying_dict['roleplayed_name'] = role.replace('{0}',
                                                                        ref_ids[attr['attribute-id']]['name'])
                                    roleplaying_dict['base_name'] = ref_ids[attr['attribute-id']]['name']

                                    if 'folder' in ref_ids[attr['attribute-id']]['properties']:
                                        roleplaying_dict['folder'] = [ref_ids[attr['attribute-id']]['properties']['folder']]
                                    else:
                                        roleplaying_dict['folder'] = [this_folder]
                                    roleplaying_dict['roleplayed_caption'] = role.replace('{0}',
                                                                    info_dict[roleplaying_dict['id']]['properties']['caption'])
                                    dim_to_id_dict[roleplaying_dict['roleplayed_name']] = roleplaying_dict

    return_dict = {}
    for i in dim_to_id_dict:
        return_dict[i] = {}

    for i in dim_to_id_dict:
        return_dict[i]['caption'] = dim_to_id_dict[i].get('roleplayed_caption', '')
        return_dict[i]['data_type'] = dim_to_id_dict[i].get('level_type', 'Standard')
        try:
            return_dict[i]['description'] = info_dict[dim_to_id_dict[i]['id']]['properties']['description']
        except KeyError:
            return_dict[i]['description'] = ''
        return_dict[i]['hierarchy'] = dim_to_id_dict[i].get('roleplayed_hierachy', [''])
        return_dict[i]['dimension'] = dim_to_id_dict[i].get('roleplayed_dimension', '')

        return_dict[i]['folder'] = dim_to_id_dict[i].get('folder', [''])
        return_dict[i]['feature_type'] = dim_to_id_dict[i].get('feature_type', 'Categorical')
        return_dict[i]['roleplay_expression'] =  dim_to_id_dict[i].get('roleplay_expression', '')
        return_dict[i]['base_name'] =  dim_to_id_dict[i].get('base_name', '')
        return_dict[i]['base_hierarchy'] =  dim_to_id_dict[i].get('base_hierarchy', '')
        return_dict[i]['base_dimension'] =  dim_to_id_dict[i].get('base_dimension', '')

        #deal with metricals
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

    cube = [x for x in project_dict['cubes']['cube'] if x['name'] == data_model_name][0]
    if 'attributes' not in cube or 'attribute' not in cube['attributes']:
        return  {}# Meaning no features have been added yet
    
    feature_info = [y for y in [x for x in cube['attributes']['attribute']]]

    for i in feature_info:
        return_dict[i['name']] = {}

    for i in feature_info:
        return_dict[i['name']]['caption'] = i.get('properties', {}).get('caption', '')
        return_dict[i['name']]['data_type'] = 'Aggregate'
        return_dict[i['name']]['description'] = i.get('properties', {}).get('description', '')
        return_dict[i['name']]['folder'] = [i.get('properties', {}).get('folder', '')]
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
        return {} # Meaning no features have been added yet

    feature_info = [x for x in project_dict['calculated-members']['calculated-member']]

    for i in feature_info:
        return_dict[i['name']] = {}

    for i in feature_info:
        return_dict[i['name']]['caption'] = i.get('properties', {}).get('caption', '')
        return_dict[i['name']]['data_type'] = 'Calculated'
        return_dict[i['name']]['description'] = i.get('properties', {}).get('description', '')
        return_dict[i['name']]['folder'] = [i.get('properties', {}).get('folder', '')]
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

    cube = [x for x in project_dict['cubes']['cube'] if x['name'] == data_model_name][0]
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
                    folder_info[level['primary-attribute']]['folder'].append(this_folder)
                    folder_info[level['primary-attribute']]['hierarchy'].append(hierarchy_name)
                else:
                    folder_info[level['primary-attribute']] = {'folder':[this_folder],
                                                            'hierarchy':[hierarchy_name],
                                                            'dimension': dimension['name']}

    for i in feature_info:
        return_dict[i['name']] = {}

    for i in feature_info:
        return_dict[i['name']]['caption'] = i.get('properties', {}).get('caption', '')
        return_dict[i['name']]['data_type'] = 'Standard'
        return_dict[i['name']]['description'] = i.get('properties', {}).get('description', '')
        return_dict[i['name']]['hierarchy'] = folder_info.get(i['id'], {}).get('hierarchy', '')
        return_dict[i['name']]['dimension'] = folder_info.get(i['id'], {}).get('dimension', '')
        return_dict[i['name']]['folder'] = folder_info.get(i['id'], {}).get('folder', '')
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
                while the inner keys are the following: 'data_type'(value is a level-type, 'Aggregate', or 'Calculated'),
                'description', 'expression', caption, 'folder', and 'feature_type'(value is Numeric or Categorical).
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
            fields=[Level.type, Level.description, Level.hierarchy, Level.caption],
            filter_by=level_filter_by
        )
        for name, info in dimension_dict.items():
            # if a level was duplicated we might have multiple hierarchies which could mean multiple folders
            folder = []
            if type(info[Level.hierarchy.name]) is list:
                for hierarchy_name in info[Level.hierarchy.name]:
                    if hier_dict.get(hierarchy_name):
                        folder.append(hier_dict[hierarchy_name][Hierarchy.folder.name])
            else:
                folder.append(hier_dict[info[Level.hierarchy.name]][Hierarchy.folder.name])
                info[Level.hierarchy.name] = [info[Level.hierarchy.name]]

            feature_dict[name] = {'caption':info[Level.caption.name],'data_type':info[Level.type.name], 'description':info[Level.description.name],
                                    'hierarchy':info[Level.hierarchy.name], 'folder':folder, 'feature_type':'Categorical'}
    if feature_type is FeatureType.ALL or feature_type is FeatureType.NUMERIC:
        catalog_licensed = data_model.project.atconn._validate_license('data_catalog_api')
        query_fields = [Measure.type, Measure.description, Measure.folder, Measure.caption]
        if catalog_licensed:
            query_fields.append(Measure.expression)
        measure_dict = get_dmv_data(
            model=data_model,
            fields=query_fields,
            filter_by=measure_filter_by
        )
        for name, info in measure_dict.items():
            feature_dict[name] = {'caption':info[Measure.caption.name],'data_type':info[Measure.type.name], 'description':info[Measure.description.name],
                                    'folder':[info[Measure.folder.name]], 'feature_type':'Numeric'}
            if catalog_licensed:
                feature_dict[name]['expression'] = info[Measure.expression.name]
            else:
                feature_dict[name]['expression'] = ''

    return feature_dict
