import re
import uuid
from typing import Optional, Union, List, Dict

from atscale.errors import atscale_errors
from atscale.parsers import project_parser, data_model_parser
from atscale.utils import model_utils, project_utils
from atscale.utils.dmv_utils import get_dmv_data
from atscale.base.enums import FeatureFormattingType, Hierarchy, Level, Aggs, MappedColumnFieldTerminator, MappedColumnKeyTerminator, MappedColumnDataTypes
from atscale.utils.input_utils import prompt_yes_no
from atscale.base.templates import (create_attribute_ref_dict, create_calculated_member_dict, create_calculated_member_ref_dict, create_keyed_attribute_dict,
                                     create_attribute_key_dict, create_attribute_key_ref_dict, create_attribute_dict,
                                     create_column_dict, create_map_column_dict, create_measure_dict)


def _create_secondary_attribute(data_model, project_dict: Dict, data_set: dict,column_name: str, new_attribute_name: str, hierarchy_name: str, level_name: str,
                               description: str = None, caption: str = None, folder: str = None, visible: bool = True):
    """Creates a new secondary attribute on an existing hierarchy and level. Edits in place.

    Args:
        data_model (DataModel): The DataModel the hierarchy is expected to belong to.
        project_dick (Dict): the dictionary representation of the project
        data_set (Dict): The dict of the dataset containing the column that the feature will use.
        column_name (str): The column that the feature will use.
        new_attribute_name (str): What the attribute will be called.
        hierarchy_name (str): What hierarchy to add the attribute to.
        level_name (str): What level of the hierarchy to add the attribute to.
        description (str, optional): The description for the attribute. Defaults to None.
        caption (str, optional): The caption for the attribute. Defaults to None.
        folder (str, optional): The folder for the attribute. Defaults to None.
        visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """

    if caption is None:
        caption = new_attribute_name

    # we do it this way so we can use pass by reference to edit the base dict
    cube_id = data_model.cube_id
    cube = project_parser.get_cube(project_dict=project_dict, id=cube_id)

    attribute_id = str(uuid.uuid4())
    ref_id = str(uuid.uuid4())

    degen = True
    if 'attributes' in project_dict and 'keyed-attribute' in project_dict['attributes']:
        for attr in project_dict['attributes']['keyed-attribute']:
            if attr['name'] == level_name:
                level_id = attr['id']
                degen = False
                break
    if 'attributes' in cube and 'keyed-attribute' in cube['attributes']:
        for attr in cube['attributes']['keyed-attribute']:
            if attr['name'] == level_name:
                level_id = attr['id']
                break

    new_attribute = create_attribute_dict(attribute_id=attribute_id)

    if degen:
        if 'dimensions' in cube and 'dimension' in cube.get('dimensions'):
            for dimension in cube['dimensions']['dimension']:
                for hier in dimension.get('hierarchy', {}):
                    if 'name' in hier and hier['name'] == hierarchy_name:
                        for l in hier.get('level', {'primary-attribute': None}):
                            if l['primary-attribute'] == level_id:
                                l.setdefault('keyed-attribute-ref', [])
                                l['keyed-attribute-ref'].append(
                                    new_attribute)

    else:
        if 'dimensions' in project_dict and 'dimension' in project_dict.get('dimensions'):
            for dimension in project_dict['dimensions']['dimension']:
                for hier in dimension.get('hierarchy', {}):
                    if 'name' in hier and hier['name'] == hierarchy_name:
                        for l in hier.get('level', {'primary-attribute': None}):
                            if l['primary-attribute'] == level_id:
                                l.setdefault('keyed-attribute-ref',  [])
                                l['keyed-attribute-ref'].append(
                                    new_attribute)

    new_ref = create_attribute_ref_dict(columns=[column_name],
                                        complete=True,
                                        attribute_id=attribute_id)

    new_keyed_attribute = create_keyed_attribute_dict(attribute_id=attribute_id,
                                                      key_ref=ref_id,
                                                      name=new_attribute_name,
                                                      visible=visible,
                                                      caption=caption,
                                                      description=description,
                                                      folder=folder,
                                                      )

    new_attribute_key = create_attribute_key_dict(
        key_id=ref_id, columns=1, visible=visible)  # in project

    new_key_ref = create_attribute_key_ref_dict(
        key_id=ref_id, columns=[column_name], complete=True, unique=False)  # in project

    data_set.setdefault('logical', {})
    data_set['logical'].setdefault('attribute-ref', [])
    data_set['logical']['attribute-ref'].append(new_ref)

    project_dict.setdefault('attributes', {})
    project_dict['attributes'].setdefault('keyed-attribute', [])
    project_dict['attributes']['keyed-attribute'].append(
        new_keyed_attribute)

    project_dict['attributes'].setdefault('attribute-key', [])
    project_dict['attributes']['attribute-key'].append(new_attribute_key)

    data_set['logical'].setdefault('key-ref', [])
    data_set['logical']['key-ref'].append(new_key_ref)

    return project_dict

def _update_secondary_attribute(project_dict: Dict, attribute_name: str, description: str = None, caption: str = None,
                                        folder: str = None) -> bool:
    """Updates the metadata for an existing secondary attribute.

    Args:
        project_dict (Dict) the dictionary representation of the project
        attribute_name (str): The name of the feature to update.
        description (str, optional): The description for the feature. Defaults to None to leave unchanged.
        caption (str, optional): The caption for the feature. Defaults to None to leave unchanged.
        folder (str, optional): The folder to put the feature in. Defaults to None to leave unchanged.
    
    Returns:
        bool: returns True if changes were made, otherwise False.
    """
    if caption == '':
        caption = attribute_name

    attributes = project_dict.get('attributes', {}).get('keyed-attribute', [])
    attribute_sub_list = [x for x in attributes if x['name'] == attribute_name]

    attribute = attribute_sub_list[0]
    any_updates = False
    if description is not None:
        attribute['properties']['description'] = description
        any_updates = True
    if caption is not None:
        attribute['properties']['caption'] = caption
        any_updates = True
    if folder is not None:
        attribute['properties']['folder'] = folder
        any_updates = True

    return any_updates
    
def _create_filter_attribute(data_model, project_dict, new_feature_name: str, level_name: str, hierarchy_name: str, filter_values: List[str],
                            caption: str = None, description: str = None, folder: str = None, visible: str = True):
    """Creates a new boolean secondary attribute to filter on a given subset of the level's values.

    Args:
        data_model (DataModel): The AtScale Data Model to run this operation on.
        project_dict (Dict): the dictionary representation of the project 
        new_feature_name (str): The name of the new feature.
        level_name (str): The name of the level to apply the filter to.
        hierarchy_name (str): The hierarchy the level belongs to.
        filter_values (List[str]): The list of values to filter on.
        caption (str): The caption for the feature. Defaults to None.
        description (str): The description for the feature. Defaults to None.
        folder (str): The folder to put the feature in. Defaults to None.
        visible (bool): Whether the created attribute will be visible to BI tools. Defaults to True.
    """
    column_id = ''
    project_dict.setdefault('attributes', {})
    project_dict['attributes'].setdefault('keyed-attribute', [])
    project_ka_list = project_dict.get(
        'attributes', {}).get('keyed_attribute', [])
    cube_ka_list = model_utils._get_model_dict(data_model, project_dict)[0].get(
        'attributes', {}).get('keyed-attribute', [])
    for keyed_attribute in project_ka_list + cube_ka_list:
        if keyed_attribute['name'] == level_name:
            column_id = keyed_attribute['id']
            break
    found = False

    project_dsets = project_parser.get_datasets(project_dict=project_dict)
    cube_dsets = data_model_parser._get_cube_datasets(
        cube_dict=model_utils._get_model_dict(data_model, project_dict)[0])
    
    for dataset in project_dsets + cube_dsets:
        for attribute in dataset.get('logical', {}).get('attribute-ref', []):
            if attribute['id'] == column_id:
                string_values = [f'\'{value}\'' for value in filter_values]
                expression = f"{attribute['column'][0]} in ({', '.join(string_values)})"
                calculated_column_name = new_feature_name + '_calc'
                project_dataset = project_parser.get_dataset_from_datasets(project_datasets=project_dsets,
                                                                           dataset_id=dataset['id'])
                dset_name = project_dataset['name']
                project_utils.create_calculated_column(atconn=data_model.project.atconn, project_dict=project_dict, data_model_id=data_model.id,
                                                       dataset_name=dset_name,
                                                       column_name=calculated_column_name,
                                                       expression=expression)

                data_set = project_parser.get_dataset_from_datasets_by_name(
                    project_parser.get_datasets(project_dict), dset_name)

                _create_secondary_attribute(data_model, project_dict, 
                                           data_set=data_set,
                                           column_name=calculated_column_name,
                                           new_attribute_name=new_feature_name,
                                           hierarchy_name=hierarchy_name,
                                           level_name=level_name, description=description, 
                                           caption=caption, folder=folder, visible=visible)
                found = True
                break
        if found:
            break

def _create_mapped_columns(dataset: Dict, column_name: str, mapped_names: List[str],
                          data_types: List[MappedColumnDataTypes], key_terminator: MappedColumnKeyTerminator, field_terminator: MappedColumnFieldTerminator,
                          map_key_type: MappedColumnDataTypes, map_value_type: MappedColumnDataTypes, first_char_delimited: bool = False):
    """Creates a mapped column.  Maps a column that is a key value structure into one or more new columns with the
    name of the given key(s). Types for the source keys and columns, and new columns are required. Valid types include
    'Int', 'Long', 'Boolean', 'String', 'Float', 'Double', 'Decimal', 'DateTime', and 'Date'. Changes are by reference

    Args:
        dataset (Dict): The dictionary representation of the dataset we're editing
        column_name (str): The name of the column.
        mapped_names (list str): The names of the mapped columns.
        data_types (list MappedColumnDataTypes): The types of the mapped columns.
        key_terminator (MappedColumnKeyTerminator): The key terminator. Valid values are ':', '=', and '^'
        field_terminator (MappedColumnFieldTerminator): The field terminator. Valid values are ',', ';', and '|'
        map_key_type (MappedColumnDataTypes): The mapping key type for all the keys in the origin column.
        map_value_type (MappedColumnDataTypes): The mapping value type for all values in the origin column.
        first_char_delimited (bool): Whether the first character is delimited. Defaults to False.
        publish (bool): Whether the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: If the given dataset or column does not exist in the data model
    """
    
    dataset['physical'].setdefault('columns', [])
    dataset['physical'].setdefault('map-column', [])

    cols = []
    for (column, type) in tuple(zip(mapped_names, data_types)):
        col = create_column_dict(name=column,
                                 data_type=type.value)
        cols.append(col)

    new_map = create_map_column_dict(columns=cols, field_terminator=field_terminator,
                                     key_terminator=key_terminator, first_char_delim=first_char_delimited,
                                     map_key_type=map_key_type, map_value_type=map_value_type,
                                     column_name=column_name)

    dataset['physical']['map-column'].append(new_map)

def _add_column_mapping(dataset: Dict, column_name: str, mapped_name: str, data_type: MappedColumnDataTypes):
    """Adds a new mapping to an existing column mapping

    Args:
        dataset (Dict): The dictionary representation of the dataset we're editing
        column_name (str): The column the mapping belongs to.
        mapped_name (MappedColumnDataTypes): The name for the new mapped column.
        data_type (str): The data type of the new mapped column.
    """
    #since all of the error handing has been handled outside of this, we can just get right to the operation
    dataset['physical'].setdefault('map-column', [])
    mapping_cols = [c for c in dataset['physical']['map-column'] if c['name'] == column_name]


    col = create_column_dict(name=mapped_name,
                             data_type=data_type.value)
    col_map = mapping_cols[0]
    col_map['columns']['columns'].append(col)

def _delete_measures_local(data_model, measure_list: List[str],
                           json_dict: Dict,
                           delete_children=None):
    """Same as delete_measure, but changes aren't pushed to AtScale. Only made on the given project_json.

     :param: measure_list the query names of the measures to be deleted
     :param: dict json_dict the project_json to be edited
     :param: delete_children Defaults to None, if set to True or False no prompt will be given in the case of
     any other measures being derived from the given measure_name. Instead, these measures will also be deleted when
     delete_children is True, alternatively, if False, the method will be aborted with no changes to the data model
     :raises: DependentMeasureException exception if child measures are encountered and the method is aborted
     :raises: UserError if measure_name is not found in the data model"""

    measure_found: Dict[str, bool] = {
        measure: False for measure in measure_list}

    calculated_members = project_parser._get_calculated_members(json_dict)

    cube = project_parser.get_cube(
        project_dict=json_dict, id=data_model.cube_id)
    try:
        cube_attributes = cube['attributes']['attribute']  # normal measures
    except KeyError:
        cube_attributes = []

    cube_calculated_member_ref = data_model_parser._get_calculated_member_refs(
        cube_dict=cube)
    datasets = data_model_parser._get_cube_datasets(cube_dict=cube)

    name_to_id: Dict[str, str] = {}
    keep_id: Dict[str, bool] = {}

    for attribute in cube_attributes:
        name = attribute['name']
        keep_id[attribute['id']] = True
        name_to_id[name] = attribute['id']
        if name in measure_found:
            if measure_found[name]:
                # Shouldn't happen 
                raise Exception(
                    f'There is more than one measure with the given query name {name}')
            else:
                measure_found[name] = True

    dependants_of: Dict[str, str] = {}

    ref_index = 0  # assuming order is the same when ignoring extra ref's not in cube
    # also assumes and cube calculated-member's id is in top level ref list
    for attribute in calculated_members:
        name = attribute['name']
        name_to_id[name] = attribute['id']
        keep_id[attribute['id']] = True
        _set_dependants(calculated_measure=attribute,
                        dependants_of=dependants_of)
        if name in measure_found:
            if measure_found[name]:
                raise Exception(
                    f'There is more than one measure with the given query name {name}')
            else:
                measure_found[name] = True
            # clear cube calculated ref from this id
            if cube_calculated_member_ref[ref_index]['id'] != attribute['id']:
                raise Exception(
                    'Cube calculated member ref not in place as expected')
        else:
            # if not in cube
            if cube_calculated_member_ref[ref_index]['id'] != attribute['id']:
                ref_index -= 1  # don't move on to next in-cube ref
        ref_index += 1

    # make sure all measures to delete were found
    for name, found in measure_found.items():
        if not found:
            raise atscale_errors.UserError(
                f'There is no measure named {name} in the data model. Make sure the measure_name'
                ' parameter is the correctly spelled query name of the measure or try refreshing '
                'the project with refresh_project')

    # retroactively set measures down family tree of measure_list to False for refiltering new lists
    for name in measure_list:
        keep_id[name_to_id[name]] = False
        new_dependants: List[str] = []
        if name in dependants_of:
            children = dependants_of[name]
            for child in children:
                if keep_id[name_to_id[child]]:
                    new_dependants.append(child)
        if new_dependants:
            if delete_children is None:
                should_delete = prompt_yes_no(f'The following measures are dependent on {name}: '
                                              f'{new_dependants} \nEnter yes to delete all of them or no to keep them'
                                              f' and abort the deletion of all measures')
            else:
                should_delete = delete_children
            if not should_delete:
                raise atscale_errors.DependentMeasureException(
                    f'Aborted deletions due to dependent measures')
            else:
                measure_list += new_dependants

    # reparse lists to remove dependancies to delete
    attributes = [feat for feat in cube_attributes if keep_id[feat['id']]]

    calculated_refs = []
    for measure in cube_calculated_member_ref:
        if keep_id[measure['id']]:
            calculated_refs.append(measure)

    new_calculated_members = []
    for measure in calculated_members:
        if keep_id[measure['id']]:
            new_calculated_members.append(measure)

    # parse datasets for removed measures attached
    for ds in datasets:
        new_features = []
        features = ds['logical'].get('attribute-ref')
        if features is None:
            break
        for feat in features:
            if feat['id'] not in keep_id or keep_id[feat['id']]:
                new_features.append(feat)
        ds['logical']['attribute-ref'] = new_features

    if 'calculated-members' in json_dict and 'calculated-member' in json_dict['calculated-members']:
        json_dict['calculated-members']['calculated-member'] = new_calculated_members
        cube['calculated-members']['calculated-member-ref'] = calculated_refs
    # do we have to delete the measure from the perspective and parent cube
    if 'attributes' in cube and 'attribute' in cube['attributes']:
        cube['attributes']['attribute'] = attributes

def _set_dependants(calculated_measure: Dict, dependants_of: Dict[str, str]):
    parents: List[str] = re.findall(pattern=r'\[Measures]\.\[[a-zA-Z0-9\_\- ]*]',
                                    string=calculated_measure['expression'])
    uses: List[str] = []
    seen: Dict[str, bool] = {}
    for big_p in parents:  # todo: optimize this by getting rid of this loop
        lil_p = big_p[12: -1]
        if not seen.get(lil_p):
            seen[lil_p] = True
            uses.append(lil_p)
    for parent in uses:
        name = calculated_measure['name']
        if parent in dependants_of:
            if name not in dependants_of[parent]:
                dependants_of[parent].append(name)
        else:
            dependants_of[parent] = [name]

def _check_hierarchy(data_model, hierarchy_name, level_name):
    hierarchy_dict = get_dmv_data(
        model=data_model,
        fields=[h for h in Hierarchy],
        id_field=Hierarchy.name
    )
    hierarchy = hierarchy_dict.get(hierarchy_name)
    if hierarchy is None:
        raise atscale_errors.UserError(
            f'Hierarchy: {hierarchy_name} does not exist in the model')
    level_dict = None
    if level_name:
        level_dict = get_dmv_data(
            model=data_model,
            fields=[l for l in Level],
            filter_by={Level.hierarchy:[hierarchy_name]},
            id_field=Level.name
        )
        level = level_dict.get(level_name)
        if level is None:
            level_dict_error_handle = get_dmv_data(
                model=data_model,
                fields=[Level.name, Level.hierarchy],
                id_field=Level.name
            )
            level_error_handle = level_dict_error_handle.get(level_name, {})
            if level_error_handle.get(Level.hierarchy.name) != hierarchy_name:
                raise atscale_errors.UserError(
                    f'Level: {level_name} does not exist in Hierarchy: {hierarchy_name}')
            raise atscale_errors.UserError(
                f'Level: {level_name} does not exist in the model')
       
    return hierarchy_dict, level_dict

def _check_time_hierarchy(data_model, hierarchy_name: str, level_name: str = None):
    """ Checks that the given hierarchy is a valid time hierarchy and (if given) that the level is in the hierarchy.
    :param DataModel data_model: The data_model the hierarchy is expected to belong to.
    :param str hierarchy_name: The name of the hierarchy to assert is a time hierarchy.
    :param str level_name: An optional name of a level to assert is in the given time_hierarchy.
    :returns Tuple A tuple with the current dmv dict of all hierarchies and the current dmv dict of all levels, in that
    order"""
    hierarchy_dict, level_dict = _check_hierarchy(data_model=data_model, hierarchy_name=hierarchy_name,
                                                  level_name=level_name)

    if hierarchy_dict[hierarchy_name][Hierarchy.type.name] != 'Time':
        raise atscale_errors.UserError(
            f'Hierarchy: {hierarchy_name} is not a time hierarchy')

    return hierarchy_dict, level_dict

def _create_calculated_feature_local(project_json: dict, cube_id: str, name, expression, description=None, caption=None,
                                     folder=None, format_string: Optional[Union[FeatureFormattingType, str]] = None,
                                     visible=True):
    if isinstance(format_string, FeatureFormattingType):
        formatting = {
            'named-format': format_string.value}
    elif format_string is None:
        formatting = None
    else:
        formatting = {
            'format-string': format_string}  # an actual format string like %DD-%m

    if caption is None:
        caption = name

    uid = str(uuid.uuid4())

    new_calc_measure = create_calculated_member_dict(id=uid, member_name=name, expression=expression,
                                                     caption=caption, visible=visible, description=description,
                                                     formatting=formatting, folder=folder)

    calculated_members = project_parser._get_calculated_members(project_json)
    calculated_members.append(new_calc_measure)

    cube = project_parser.get_cube(project_dict=project_json,
                                   id=cube_id)

    new_ref = create_calculated_member_ref_dict(id=uid)
    calculated_members_refs = data_model_parser._get_calculated_member_refs(
        cube)
    calculated_members_refs.append(new_ref)

def _update_calculated_feature(project_dict: Dict, feature_name: str, expression: str = None, description: str = None, caption: str = None,
                              folder: str = None, format_string: Optional[Union[FeatureFormattingType, str]] = None,
                              visible: bool = None):
    """Update the metadata for a calculated feature.

    Args:
        project_dict (Dict) the dictionary representation of the project
        feature_name (str): The name of the feature to update.
        expression (str): The expression for the feature. Defaults to None to leave unchanged.
        description (str): The description for the feature. Defaults to None to leave unchanged.
        caption (str): The caption for the feature. Defaults to None to leave unchanged.
        folder (str): The folder to put the feature in. Defaults to None to leave unchanged.
        format_string (str): The format string for the feature. Defaults to None to leave unchanged.
        visible (bool): Whether the updated feature should be visible. Defaults to None to leave unchanged.
    """

    if isinstance(format_string, FeatureFormattingType):
        formatting = {
            'named-format': format_string.value}
    else:
        formatting = {
            'format-string': format_string}  # an actual format string like %DD-%m or None

    if caption == '':
        caption = feature_name

    measure = [x for x in project_dict['calculated-members']
               ['calculated-member'] if x['name'] == feature_name][0]

    measure.setdefault('properties', {})
    if expression is not None:
        measure['expression'] = expression
    if description is not None:
        measure['properties']['description'] = description
    if caption is not None:
        measure['properties']['caption'] = caption
    if folder is not None:
        measure['properties']['folder'] = folder
    if visible is not None:
        measure['properties']['visible'] = visible
    if format_string is not None:
        if format_string == '':
            measure['properties'].pop('formatting', not_found=None)
        else:
            measure['properties']['formatting'] = formatting

def _create_aggregate_feature_local(project_json: dict, cube_id: str, dataset_name: str, column_name: str, name: str, 
                            aggregation_type: Aggs, description: str = None, caption: str = None, folder: str = None,
                            format_string: Optional[Union[FeatureFormattingType, str]] = None, visible: bool = True):

    aggregation_str = ''
    if not isinstance(aggregation_type, Aggs):
        aggregation_type_caps = aggregation_type.upper()

        if aggregation_type_caps not in Aggs._member_names_:
            raise Exception(
                f'Invalid aggregation_type: \'{aggregation_type}\'. Valid options are: {Aggs._member_names_}. or string utils.Aggs member')
        else:
            aggregation_str = aggregation_type_caps
    else:
        aggregation_str = aggregation_type.value

    if isinstance(format_string, FeatureFormattingType):
        formatting = {
            'named-format': format_string.value}
    elif format_string is None:
        formatting = None
    else:
        formatting = {
            'format-string': format_string}  # an actual format string like %DD-%m

    if caption is None:
        caption = name

    uid = str(uuid.uuid4())

    cube = project_parser.get_cube(project_dict=project_json,
                                   id=cube_id)

    new_measure = create_measure_dict(measure_id=uid, measure_name=name,
                                      agg_str=aggregation_str, caption=caption, visible=visible,
                                      description=description, formatting=formatting, folder=folder)

    cube.setdefault('attributes', {})
    cube['attributes'].setdefault('attribute', [])
    cube['attributes']['attribute'].append(new_measure)

    data_set_project = project_parser.get_dataset_from_datasets_by_name(project_parser.get_datasets(project_json),
                                                                        dataset_name)
    data_set_id = data_set_project.get('id')
    dataset: dict = [x for x in cube['data-sets']
                     ['data-set-ref'] if x['id'] == data_set_id][0]

    new_ref = create_attribute_ref_dict(columns=[column_name], attribute_id=uid,
                                        complete=True)

    dataset.setdefault('logical', {})
    dataset['logical'].setdefault('attribute-ref', [])
    dataset['logical']['attribute-ref'].append(new_ref)

def _update_aggregate_feature(project_dict: Dict, cube_id: str, feature_name: str, 
                                    description: str = None, caption: str = None,
                                      folder: str = None,
                                      format_string: Optional[Union[FeatureFormattingType, str]] = None,
                                      visible: bool = None):
    """Update the metadata for an aggregate feature.

    Args:
        project_dict (Dict) the dictionary representation of the project
        cube_id (str): the id of the cube.
        feature_name (str): The name of the feature to update.
        description (str): The description for the feature. Defaults to None to leave unchanged.
        caption (str): The caption for the feature. Defaults to None to leave unchanged.
        folder (str): The folder to put the feature in. Defaults to None to leave unchanged.
        format_string (str): The format string for the feature. Defaults to None to leave unchanged.
        visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to None to leave unchanged.
    """


    if isinstance(format_string, FeatureFormattingType):
        formatting = {
            'named-format': format_string.value}
    else:
        formatting = {
            'format-string': format_string}

    if caption == '':
        caption = feature_name

    cube = project_parser.get_cube(project_dict=project_dict,
                                   id=cube_id)

    measure = [x for x in cube['attributes']
               ['attribute'] if x['name'] == feature_name][0]
    measure.setdefault('properties', {})

    if description is not None:
        measure['properties']['description'] = description
    if caption is not None:
        measure['properties']['caption'] = caption
    if folder is not None:
        measure['properties']['folder'] = folder
    if visible is not None:
        measure['properties']['visible'] = visible
    if format_string is not None:
        if format_string == '':
            measure['properties'].pop('formatting', not_found=None)
        else:
            measure['properties']['formatting'] = formatting

def _create_rolling_agg(project_json, cube_id, time_dimension, agg_type, new_feature_name, 
                           numeric_feature_name,  time_length, hierarchy_name, level_name,
                           description, caption, folder, format_string, visible):
    """ Factors out common code from several of the following functions that create calculated features.

    :param dict project_json: The project dict to write the feature into
    :param str cube_id: the id of the cube to write into
    :param str time_dimension: the time dimension for the given hierarchy 
    :param MDXAgg agg_type: the type of aggregation to use
    :param str new_feature_name: What the feature will be called.
    :param str numeric_feature_name: The numeric feature to use for the calculation.
    :param int time_length: The length of time the feature should be calculated over.
    :param str hierarchy_name: The time hierarchy used in the calculation.
    :param str level_name: The level within the time hierarchy.
    :param str description: The description for the feature.
    :param str caption: The caption for the feature.
    :param str folder: The folder to put the feature in.
    :param str format_string: The format string for the feature.
    :param bool visible: Whether the feature will be visible to BI tools. Defaults to True.
    """

    from atscale.utils import feature_utils

    expression = agg_type.value + f'(' \
                                f'ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}]' \
                                f', {time_length - 1}, [{time_dimension}].[{hierarchy_name}].CurrentMember)' \
                                f':[{time_dimension}].[{hierarchy_name}].CurrentMember, [Measures].[{numeric_feature_name}])'

    feature_utils._create_calculated_feature_local(project_json, cube_id=cube_id, name = new_feature_name, 
                              expression = expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible)
    # todo: use create_calculated_feature_local
    return f'Successfully created measure \'{new_feature_name}\' {f"in folder {folder}" if folder else ""}'

def _create_lag_feature_local(project_dict: Dict, cube_id: str, time_dimension: str, 
               new_feature_name: str, numeric_feature_name: str,  time_length: int,
               hierarchy_name: str, level_name: str,
               description: str = None, caption: str = None, folder: str = None, format_string: str = None, visible: bool = True):
    """Creates a lagged feature based on the numeric feature and time hierachy passed in.

    Args:
        project_dict (Dict): the dictionary representation of the project of interest
        cube_id (str): the unique idenitifier for this cube
        time_dimension (str): the query name of the time dimension we lag over 
        new_feature_name (str): The name of the feature to create.
        numeric_feature_name (str): The numeric feature to lag.
        time_length (int): The length of the lag.
        hierarchy_name (str): The time hierarchy to use for the lag.
        level_name (str): The level of the hierarchy to use for the lag.
        description (str, optional): A description for the feature. Defaults to None.
        caption (str, optional): A caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): A format sting for the feature. Defaults to None.
        visible (bool, optional): Whether the feature should be visible. Defaults to True.
        publish (bool, optional): Whether to publish the project after creating the feature. Defaults to True.

    Raises:
        atscale_errors.UserError: If an invalid length (not an Integer greater than 0) is passed
    """

    expression = f'(ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}], {time_length}' \
                 f', [{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}])'

    _create_calculated_feature_local(project_dict, cube_id= cube_id, name = new_feature_name, expression = expression, 
                              description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible)

def _create_time_differencing_feature_local(project_dict: Dict, cube_id: str, time_dimension: str, 
                             new_feature_name: str, numeric_feature_name: str, time_length: int,
                             hierarchy_name: str, level_name: str, description: str = None, caption: str = None,
                             folder: str = None, format_string: Optional[Union[str, FeatureFormattingType]] = None,
                             visible: bool = True):
    """Creates a time over time subtraction calculation. For example, create_time_differencing on the feature 'revenue'
    , time level 'date', and a length of 2 will create a feature calculating the revenue today subtracted by the revenue
     two days ago

    Args:
        project_dict (Dict): the dictionary representation of the project of interest
        cube_id (str): the unique idenitifier for this cube
        time_dimension (str): the query name of the time dimension we lag over 
        new_feature_name (str): What the feature will be called.
        numeric_feature_name (str): The numeric feature to use for the calculation.
        length (int): The length of the lag in units of the given level of the given time_hierarchy.
        hierarchy_name (str): The time hierarchy used in the calculation.
        level_name (str): The level within the time hierarchy
        description (str): The description for the feature. Defaults to None.
        caption (str): The caption for the feature. Defaults to None.
        folder (str): The folder to put the feature in. Defaults to None.
        format_string (str): The format string for the feature. Defaults to None.
    """
    expression = f'CASE WHEN IsEmpty((ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}], {time_length}' \
                 f', [{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}])) ' \
                 f'THEN 0 ELSE ([Measures].[{numeric_feature_name}]' \
                 f'-(ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}], {time_length}' \
                 f', [{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}])) END'


    _create_calculated_feature_local(project_json=project_dict,
                                     cube_id=cube_id,
                                     name=new_feature_name,
                                     expression=expression,
                                     description=description, caption=caption, folder=folder,
                                     format_string=format_string, visible=visible)

def _create_percentage_feature_local(project_dict, cube_id, new_feature_name, numeric_feature_name, dimension_name, hierarchy_name, level_name,
                             description=None, caption=None, folder=None, format_string=None, visible=True):
    expression = f'IIF( (Ancestor([{dimension_name}].[{hierarchy_name}].currentMember' \
                 f', [{dimension_name}].[{hierarchy_name}].[{level_name}]), ' \
                 f'[Measures].[{numeric_feature_name}]) = 0, NULL, ' \
                 f'[Measures].[{numeric_feature_name}]' \
                 f' / (Ancestor([{dimension_name}].[{hierarchy_name}].currentMember' \
                 f', [{dimension_name}].[{hierarchy_name}].[{level_name}]), [Measures].[{numeric_feature_name}]))'
    _create_calculated_feature_local(project_json=project_dict, cube_id=cube_id, name=new_feature_name, expression=expression,
                                     description=description, caption=caption, folder=folder,
                                     format_string=format_string, visible=visible)

def _create_period_to_date_feature_local(project_dict, cube_id, new_feature_name, numeric_feature_name: str, hierarchy_name: str,  
                           level_name, base_name, time_dimension, description: str = None,
                           folder: str = None, format_string: str = None, visible: bool = True):
    """Creates a period-to-date calculation
    """
    true_description = f'A sum of {numeric_feature_name} from all {base_name} entries in the past ' \
                        f'{level_name}. \n {description if description else ""}'
    expression = f'CASE WHEN IsEmpty([Measures].[{numeric_feature_name}]) THEN NULL ELSE ' \
                    f'Sum(PeriodsToDate([{time_dimension}].[{hierarchy_name}].[{level_name}], ' \
                    f'[{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}]) END'
    _create_calculated_feature_local(project_json=project_dict, cube_id=cube_id, name= new_feature_name,
                                        expression=expression, description=true_description, caption=None,
                                        folder=folder, format_string=format_string, visible=visible)
