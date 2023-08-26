import json
import re
import uuid
from typing import Optional, Union, List, Dict
from pandas import DataFrame

from atscale.errors import atscale_errors
from atscale.base import templates
from atscale.connection.connection import Connection
from atscale.data_model.data_model import DataModel
from atscale.parsers import project_parser, data_model_parser
from atscale.utils import dimension_utils, project_utils
from atscale.utils.dmv_utils import get_dmv_data
from atscale.base.enums import FeatureFormattingType, Hierarchy, Level, Measure, MDXAggs, Aggs, TimeSteps, RequestType
from atscale.utils.input_utils import prompt_yes_no
from atscale.utils.model_utils import check_features
from atscale.base.templates import (create_attribute_ref_dict, create_calculated_member_dict, create_calculated_member_ref_dict, create_dimension_dict, create_hierarchy_dict, create_keyed_attribute_dict,
                                     create_attribute_key_dict, create_attribute_key_ref_dict, create_attribute_dict,
                                     create_column_dict, create_map_column_dict, create_measure_dict, create_hierarchy_level_dict)


def create_secondary_attribute(data_model: DataModel, dataset_name: str, column_name: str, new_attribute_name: str, hierarchy_name: str, level_name: str,
                               description: str = None, caption: str = None, folder: str = None, visible: bool = True, publish: bool = True):
    """Creates a new secondary attribute on an existing hierarchy and level.

    Args:
        data_model (DataModel): The DataModel the hierarchy is expected to belong to.
        dataset_name (str): The dataset containing the column that the feature will use.
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

    project_json = data_model.project._get_dict()

    if new_attribute_name in list(data_model.get_features()['name']):
        raise atscale_errors.UserError(
            f'Invalid name: \'{new_attribute_name}\'. A feature already exists with that name')

    data_set = project_parser.get_dataset_from_datasets_by_name(project_parser.get_datasets(project_json),
                                                                dataset_name)
    if not data_set:
        raise atscale_errors.UserError(
            f'Dataset \'{dataset_name}\' not associated with given project')

    data_set['physical'].setdefault('columns', [])
    dset_columns = [c['name'] for c in data_set['physical']['columns']]

    check_features(features=[column_name],
                   check_list=dset_columns,
                   errmsg=f'Invalid parameter: column name \'{column_name}\' does not exist in'
                   f' dataset \'{dataset_name}\'')

    _check_hierarchy(data_model=data_model, hierarchy_name=hierarchy_name,
                     level_name=level_name)
    if caption is None:
        caption = new_attribute_name

    # we do it this way so we can use pass by reference to edit the base dict
    cube_id = data_model.cube_id
    cube = project_parser.get_cube(project_dict=project_json, id=cube_id)

    attribute_id = str(uuid.uuid4())
    ref_id = str(uuid.uuid4())

    degen = True
    if 'attributes' in project_json and 'keyed-attribute' in project_json['attributes']:
        for attr in project_json['attributes']['keyed-attribute']:
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
        if 'dimensions' in project_json and 'dimension' in project_json.get('dimensions'):
            for dimension in project_json['dimensions']['dimension']:
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

    project_json.setdefault('attributes', {})
    project_json['attributes'].setdefault('keyed-attribute', [])
    project_json['attributes']['keyed-attribute'].append(
        new_keyed_attribute)

    project_json['attributes'].setdefault('attribute-key', [])
    project_json['attributes']['attribute-key'].append(new_attribute_key)

    data_set['logical'].setdefault('key-ref', [])
    data_set['logical']['key-ref'].append(new_key_ref)

    data_model.project._update_project(
        project_json=project_json, publish=publish)


def update_secondary_attribute_metadata(data_model: DataModel, attribute_name: str, description: str = None, caption: str = None,
                                        folder: str = None, publish: bool = True):
    """Updates the metadata for an existing secondary attribute.

    Args:
        data_model (DataModel): The DataModel the feature is expected to belong to.
        attribute_name (str): The name of the feature to update.
        description (str, optional): The description for the feature. Defaults to None to leave unchanged.
        caption (str, optional): The caption for the feature. Defaults to None to leave unchanged.
        folder (str, optional): The folder to put the feature in. Defaults to None to leave unchanged.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    project_json = data_model.project._get_dict()

    if caption == '':
        caption = attribute_name

    attributes = project_json.get('attributes', {}).get('keyed-attribute', [])
    if len(attributes) < 1:
        raise Exception(f'No secondary attributes found.')

    attribute_sub_list = [x for x in attributes if x['name'] == attribute_name]
    if len(attribute_sub_list) < 1:
        raise Exception(
            f'Secondary Attribute: {attribute_name} does not exist.')

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

    if(any_updates):
        data_model.project._update_project(
            project_json=project_json, publish=publish)


def create_filter_attribute(data_model: DataModel, new_feature_name: str, level_name: str, hierarchy_name: str, filter_values: List[str],
                            caption: str = None, description: str = None,
                            folder: str = None, visible: str = True, publish: str = True):
    """Creates a new boolean secondary attribute to filter on a given subset of the level's values.

    Args:
        data_model (DataModel): The AtScale Data Model to run this operation on.
        new_feature_name (str): The name of the new feature.
        level_name (str): The name of the level to apply the filter to.
        hierarchy_name (str): The hierarchy the level belongs to.
        filter_values (List[str]): The list of values to filter on.
        caption (str): The caption for the feature. Defaults to None.
        description (str): The description for the feature. Defaults to None.
        folder (str): The folder to put the feature in. Defaults to None.
        visible (bool): Whether the created attribute will be visible to BI tools. Defaults to True.
        publish (bool): Whether or not the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: If a feature already exists with the given name.
    """
    column_id = ''
    project_dict = data_model.project._get_dict()
    project_dict.setdefault('attributes', {})
    project_dict['attributes'].setdefault('keyed-attribute', [])
    project_ka_list = project_dict.get(
        'attributes', {}).get('keyed_attribute', [])
    cube_ka_list = data_model._get_model_dict()[0].get(
        'attributes', {}).get('keyed-attribute', [])
    for keyed_attribute in project_ka_list + cube_ka_list:
        if keyed_attribute['name'] == level_name:
            column_id = keyed_attribute['id']
            break
    found = False
    project_dsets = project_parser.get_datasets(project_dict=project_dict)
    cube_dsets = data_model_parser._get_cube_datasets(
        cube_dict=data_model._get_model_dict()[0])
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
                # JTL - we're hitting the server too much. I think utils methods should generally be operating with dicts to create and mutate things, not having objects and hitting the server.
                # There are of course exceptions. Parsers also should only work with dicts. "Orchestrating methods" should generally be the ones hitting the server. Generally speaking, I think
                # orchestrating methods are those in client, project, data_model, atconn, (we may need more). I had to put in the line below because this used to be called in model_utils
                # within create calculated feature but I really wanted that to only work with dict objects so calling methods have more optionality of if/when to hit the server when you're doing
                # several mutations. We should decouple that a bit more so orchestrating methods get to decide when to hit the server and it's not forced on every mutation. But trying to go fast,
                # so leaving this here for now (because I imagine the call right below it also hits the server and there's too much to change at a single time). TODO: I'd reccomend going back over
                # this method and making it such that the call to the server to update project only happens at the end. Albeit - this is in feature_utils, so really it probably shouldn't be in here
                # at all. This method should likely just mutated the dict, and then whatever calls this should be responsible for updating the project.
                data_model.project._update_project(
                    project_json=project_dict, publish=publish)
                create_secondary_attribute(data_model=data_model,
                                           dataset_name=dset_name,
                                           column_name=calculated_column_name,
                                           new_attribute_name=new_feature_name,
                                           hierarchy_name=hierarchy_name,
                                           level_name=level_name,
                                           description=description, caption=caption, folder=folder, visible=visible,
                                           publish=publish)
                found = True
                break
        if found:
            break


def generate_time_series_features(data_model: DataModel, dataframe: DataFrame, numeric_features: List[str], time_hierarchy: str, level: str, group_features: List[str] = None,
                                  intervals: List[int] = None, shift_amount: int = 0) -> DataFrame:
    """Generates time series features like rolling statistics and period to date for the given numeric features
     using the time hierarchy from the given data model

    Args:
        data_model (DataModel): The data model to use.
        dataframe (DataFrame): the dataframe with the features.
        numeric_features (List[str]): The list of numeric features to build time series features of.
        time_hierarchy (str): The time hierarchy to use to derrive features.
        level (str): The level of the time hierarchy to derive the features at.
        group_features (List[str], optional): _description_. Defaults to None.
        intervals (List[int], optional): The intervals to create the features over. 
        Will use default values based on the time step of the given level if None. Defaults to None.
        shift_amount (int, optional): The amount of rows to shift the new features. Defaults to 0.

    Returns:
        DataFrame: A DataFrame containing the original columns and the newly generated ones
    """
    _check_time_hierarchy(data_model=data_model,
                          hierarchy_name=time_hierarchy, level_name=level)

    measure_list = list(get_dmv_data(
        model=data_model, id_field=Measure.name).keys())
    level_dict = get_dmv_data(model=data_model, fields=[Level.name, Level.type],
                              filter_by={Level.hierarchy: [time_hierarchy]})
    level_list = list(level_dict.keys())
    if group_features:
        if type(group_features) != list:
            group_features = [group_features]
        check_features(group_features, measure_list + level_list)

    if type(numeric_features) != list:
        numeric_features = [numeric_features]
    check_features(numeric_features, measure_list,
                   errmsg='Make sure all items in numeric_features are numeric features')

    time_numeric = level_dict[level][Level.type.name]
    # takes out the Time and 's' at the end and in lowercase
    time_name = str(time_numeric)[4:-1].lower()

    if intervals:
        if type(intervals) != list:
            intervals = [intervals]
    else:
        intervals = TimeSteps[time_numeric].value

    shift_name = f'_shift_{shift_amount}' if shift_amount != 0 else ''

    levels = [x for x in level_list if x in dataframe.columns]

    if group_features:
        dataframe = dataframe.sort_values(
            by=group_features + levels).reset_index(drop=True)
    else:
        dataframe = dataframe.sort_values(by=levels).reset_index(drop=True)

    for feature in numeric_features:
        for interval in intervals:
            interval = int(interval)
            name = feature + f'_{interval}_{time_name}_'
            if group_features:
                def grouper(x): return x.groupby(group_features)
            else:
                def grouper(x): return x
                # set this to an empty list so we can add it to hier_level later no matter what
                group_features = []
            if interval > 1:
                dataframe[f'{name}sum{shift_name}'] = grouper(dataframe)[feature].rolling(
                    interval).sum().shift(shift_amount).reset_index(drop=True)

                dataframe[f'{name}avg{shift_name}'] = grouper(dataframe)[feature].rolling(
                    interval).mean().shift(shift_amount).reset_index(drop=True)

                dataframe[f'{name}stddev{shift_name}'] = grouper(dataframe)[feature].rolling(
                    interval).std().shift(shift_amount).reset_index(drop=True)

                dataframe[f'{name}min{shift_name}'] = grouper(dataframe)[feature].rolling(
                    interval).min().shift(shift_amount).reset_index(drop=True)

                dataframe[f'{name}max{shift_name}'] = grouper(dataframe)[feature].rolling(
                    interval).max().shift(shift_amount).reset_index(drop=True)

            dataframe[f'{name}lag{shift_name}'] = grouper(dataframe)[feature].shift(
                interval).shift(shift_amount).reset_index(drop=True)

        found = False
        for heir_level in reversed(levels):
            if found and heir_level in dataframe.columns:
                name = f'{feature}_{heir_level}_to_date'
                dataframe[name] = dataframe.groupby(
                    group_features + [heir_level])[feature].cumsum().shift(1).reset_index(drop=True)
            if heir_level == level:
                found = True

    return dataframe


def create_mapped_columns(data_model: DataModel, dataset_name: str, column_name: str, mapped_names: List[str],
                          data_types: List[str], key_terminator: str, field_terminator: str,
                          map_key_type: str, map_value_type: str, first_char_delimited: bool = False,
                          publish: bool = True):
    """Creates a mapped column.  Maps a column that is a key value structure into one or more new columns with the
    name of the given key(s). Types for the source keys and columns, and new columns are required. Valid types include
    'Int', 'Long', 'Boolean', 'String', 'Float', 'Double', 'Decimal', 'DateTime', and 'Date'.

    Args:
        data_model (DataModel): The AtScale Data Model that the operation will occur on.
        dataset_name (str): The dataset the mapped column will be derived in.
        column_name (str): The name of the column.
        mapped_names (list str): The names of the mapped columns.
        data_types (list str): The types of the mapped columns.
        key_terminator (str): The key terminator. Valid values are ':', '=', and '^'
        field_terminator (str): The field terminator. Valid values are ',', ';', and '|'
        map_key_type (str): The mapping key type for all the keys in the origin column.
        map_value_type (str): The mapping value type for all values in the origin column.
        first_char_delimited (bool): Whether the first character is delimited. Defaults to False.
        publish (bool): Whether the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: If the given dataset or column does not exist in the data model
    """

    valid_key_terminators = [':', '=', '^']
    if key_terminator not in valid_key_terminators:
        raise Exception(
            f'Invalid key_terminator: `{key_terminator}` valid values are `:`, `=`, and `^`')
    valid_field_terminators = [',', ';', '|']
    if field_terminator not in valid_field_terminators:
        raise Exception(
            f'Invalid field_terminator: `{field_terminator}` valid values are `,`, `;`, and `|`')

    valid_types = ['Int', 'Long', 'Boolean', 'String', 'Float',
                   'Double', 'Decimal', 'DateTime', 'Date']
    for type in data_types:
        if type not in valid_types:
            raise Exception(f'Invalid data_type: `{type}` valid values are `Int`, `Long`, `Boolean`, `String`, '
                            f'`Float`, `Double`, `Decimal`, `DateTime`, `Date`')

    project_dict = data_model.project._get_dict()
    cube_dict = data_model._get_model_dict()[0]

    dset = project_parser.get_dataset_from_datasets_by_name(
        project_datasets=data_model_parser.get_project_datasets_referenced_by_cube(project_dict=project_dict,
                                                                                   cube_dict=cube_dict),
        dataset_name=dataset_name)
    if not dset:
        raise atscale_errors.UserError(f'Invalid parameter: dataset name {dataset_name} does not exist or is not '
                                       f'used in the data model yet')
    dset['physical'].setdefault('columns', [])
    dset_columns = [c['name'] for c in dset['physical']['columns']]
    check_features(features=[column_name],
                   check_list=dset_columns,
                   errmsg=f'Invalid parameter: column name \'{column_name}\' does not exist in'
                          f' dataset \'{dataset_name}\'')

    dset['physical'].setdefault('map-column', [])

    cols = []
    for (column, type) in tuple(zip(mapped_names, data_types)):
        col = create_column_dict(name=column,
                                 data_type=type)
        cols.append(col)

    new_map = create_map_column_dict(columns=cols, field_terminator=field_terminator,
                                     key_terminator=key_terminator, first_char_delim=first_char_delimited,
                                     map_key_type=map_key_type, map_value_type=map_value_type,
                                     column_name=column_name)

    dset['physical']['map-column'].append(new_map)

    data_model.project._update_project(
        project_json=project_dict, publish=publish)


def add_column_mapping(data_model: DataModel, dataset_name: str, column_name: str, mapped_name: str, data_type: str, publish: bool = True):
    """Adds a new mapping to an existing column mapping

    Args:
        data_model (DataModel): The data model to update.
        dataset_name (str): The dataset the mapping belongs to.
        column_name (str): The column the mapping belongs to.
        mapped_name (str): The name for the new mapped column.
        data_type (str): The data type of the new mapped column.
        publish (bool, optional): _description_. Defaults to True.

    Raises:
        atscale_errors.UserError: If there isn't already a column mapping for the dataset to update.
        atscale_errors.UserError: If there is already a mapping with the same name.
    """

    valid_types = ['Int', 'Long', 'Boolean', 'String', 'Float',
                   'Double', 'Decimal', 'DateTime', 'Date']
    if data_type not in valid_types:
        raise Exception(f'Invalid data_type: `{data_type}` valid values are `Int`, `Long`, `Boolean`, '
                        f'`String`, `Float`, `Double`, `Integer`, `Decimal`, `DateTime`, `Date`')

    project_dict = data_model.project._get_dict()
    cube_dict = data_model._get_model_dict()[0]

    dset = project_parser.get_dataset_from_datasets_by_name(
        project_datasets=data_model_parser.get_project_datasets_referenced_by_cube(project_dict=project_dict,
                                                                                   cube_dict=cube_dict),
        dataset_name=dataset_name)
    if not dset:
        raise atscale_errors.UserError(f'Invalid parameter: dataset \'{dataset_name}\' does not exist or is not '
                                       f'used in the data model yet')
    dset['physical'].setdefault('columns', [])
    dset_columns = [c['name'] for c in dset['physical']['columns']]
    check_features(features=[column_name],
                   check_list=dset_columns,
                   errmsg=f'Invalid parameter: column name \'{column_name}\' does not exist in'
                          f' dataset \'{dataset_name}\'')

    if 'map-column' not in dset['physical']:
        raise atscale_errors.UserError(
            f'No mapped column exists in the dataset. Use create_mapped_columns to create one')
    mapping_cols = [c for c in dset['physical']
                    ['map-column'] if c['name'] == column_name]
    if len(mapping_cols) < 1:
        raise atscale_errors.UserError(f'No mapped column exists for column: {mapped_name}. Use create_mapped_columns '
                                       f'to create one')
    already_mapped_w_name = [col for col in mapping_cols[0]
                             ['columns']['columns'] if col['name'] == mapped_name]
    if already_mapped_w_name:
        raise atscale_errors.UserError(
            f'There is already a mapping on column \'{column_name}\' for the key \'{mapped_name}\'')
    # todo: raise error if mapping conflicts with normal column?

    col = create_column_dict(name=mapped_name,
                             data_type=data_type)
    col_map = mapping_cols[0]
    col_map['columns']['columns'].append(col)

    data_model.project._update_project(
        project_json=project_dict, publish=publish)


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
                # won't happen
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
            id_field=Level.name
        )
        level = level_dict.get(level_name)
        if level is None:
            raise atscale_errors.UserError(
                f'Level: {level_name} does not exist in the model')
        if level.get(Level.hierarchy.name) != hierarchy_name:
            raise atscale_errors.UserError(
                f'Level: {level_name} does not exist in Hierarchy: {hierarchy_name}')
    return hierarchy_dict, level_dict


def _check_time_hierarchy(data_model: DataModel, hierarchy_name: str, level_name: str = None):
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


def create_calculated_feature(data_model: DataModel, new_feature_name: str, expression: str, description: str = None,
                              caption: str = None, folder: str = None,
                              format_string: Optional[Union[FeatureFormattingType, str]] = None, visible: bool = True,
                              publish: bool = True):
    """Creates a new calculated feature given a name and an MDX Expression.

    Args:
        data_model (DataModel): the DataModel object to work with.
        new_feature_name (str): What the feature will be called.
        expression (str): The MDX expression for the feature.
        description (str): The description for the feature. Defaults to None.
        caption (str): The caption for the feature. Defaults to None.
        folder (str): The folder to put the feature in. Defaults to None.
        format_string (str): The format string for the feature. Defaults to None.
        visible (bool): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool): Whether the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: If a feature already exists with the given name
    """
    project_json = data_model.project._get_dict()
    _create_calculated_feature_local(project_json=project_json,
                                     cube_id=data_model.cube_id,
                                     name=new_feature_name,
                                     expression=expression,
                                     description=description,
                                     caption=caption,
                                     folder=folder,
                                     format_string=format_string,
                                     visible=visible)

    if new_feature_name in list(data_model.get_features()['name']):
        raise atscale_errors.UserError(
            f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')

    data_model.project._update_project(
        project_json=project_json, publish=publish)


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


def update_calculated_feature_metadata(data_model: DataModel, feature_name: str, description: str = None, caption: str = None,
                                       folder: str = None, format_string: Optional[Union[FeatureFormattingType, str]] = None,
                                       visible: bool = None, publish: bool = True):
    """Update the metadata for a calculated feature.

    Args:
        data_model (DataModel): the atscale datamodel object to work with
        feature_name (str): The name of the feature to update.
        description (str): The description for the feature. Defaults to None to leave unchanged.
        caption (str): The caption for the feature. Defaults to None to leave unchanged.
        folder (str): The folder to put the feature in. Defaults to None to leave unchanged.
        format_string (str): The format string for the feature. Defaults to None to leave unchanged.
        visible (bool): Whether the updated feature should be visible. Defaults to None to leave unchanged.
        publish (bool): Whether the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: If the given name parameter does not match name in the data model
    """

    # calculated_measure_matches = get_dmv_data(atmodel, [Measure.type], filter_by =
    #                                 {Measure.type: ['Calculated']})

    calculated_measure_matches = get_dmv_data(data_model, [Measure.type], filter_by={
        Measure.type: ['Calculated'],
        Measure.name: [feature_name]})

    if not len(calculated_measure_matches):
        raise atscale_errors.UserError(
            f'Invalid name: \'{feature_name}\'. A feature with that name does not exist')

    if isinstance(format_string, FeatureFormattingType):
        formatting = {
            'named-format': format_string.value}
    else:
        formatting = {
            'format-string': format_string}  # an actual format string like %DD-%m or None

    if caption == '':
        caption = feature_name

    project_json = data_model.project._get_dict()
    measure = [x for x in project_json['calculated-members']
               ['calculated-member'] if x['name'] == feature_name][0]

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

    data_model.project._update_project(
        project_json=project_json, publish=publish)


def create_denormalized_categorical_feature(data_model: DataModel, dataset_name: str, column_name: str, name: str, description: str = None,
                                            caption: str = None, folder: str = None, visible: bool = True, publish: bool = True):
    """Creates a new denormalized categorical feature.

    Args:
        data_model (DataModel): The datamodel containing the dataset and column_name that the feature will use.
        dataset_name (str): The name of the dataset to find the column_name.
        column_name (str): The column that the feature will use.
        name (str): What the feature will be called.
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """

    if name in list(data_model.get_features()['name']):
        raise atscale_errors.UserError(
            f'Invalid name: \'{name}\'. A feature already exists with that name')

    if not data_model.dataset_exists(dataset_name):
        raise atscale_errors.UserError(
            f'Dataset \'{dataset_name}\' not associated with given model')

    if not data_model.column_exists(dataset_name, column_name):
        raise atscale_errors.UserError(
            f'Column \'{column_name}\' not found in the \'{dataset_name}\' dataset')

    atconn = data_model.project.atconn
    project_dict = data_model.project._get_dict()
    data_set_project = project_parser.get_dataset_from_datasets_by_name(project_parser.get_datasets(project_dict),
                                                                        dataset_name)
    dataset_id = data_set_project.get('id')
    dimension_utils.create_categorical_dimension_for_column(atconn=atconn, project_dict=project_dict, data_model_id=data_model.id, dataset_id=dataset_id,
                                                            column_name=column_name, name=name, description=description, caption=caption, folder=folder, visible=visible)
    data_model.project._update_project(
        project_json=project_dict, publish=publish)


def create_aggregate_feature(data_model: DataModel, dataset_name: str, column_name: str, name: str, aggregation_type: Aggs,
                             description: str = None, caption: str = None, folder: str = None,
                             format_string: Optional[Union[FeatureFormattingType, str]] = None, visible: bool = True, publish: bool = True):
    """Creates a new aggregate feature.

    Args:
        data_model (DataModel): the atscale datamodel object to work with
        dataset_name (str): The dataset containing the column that the feature will use.
        column_name (str): The column that the feature will use.
        name (str): What the feature will be called.
        aggregation_type (atscale.utils.enums.Aggs): What aggregation method to use for the feature. Example: Aggs.MAX
            Valid options can be found in utils.Aggs
        description (str): The description for the feature. Defaults to None.
        caption (str): The caption for the feature. Defaults to None.
        folder (str): The folder to put the feature in. Defaults to None.
        format_string: The format string for the feature. Defaults to None.
        visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to True.
        publish (bool): Whether or not the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: If the given name is already used in the data_model.
        Exception: If the aggregation type is not an Aggs enum.
    """
    if name in list(data_model.get_features()['name']):
        raise atscale_errors.UserError(
            f'Invalid name: \'{name}\'. A feature already exists with that name')

    if not data_model.dataset_exists(dataset_name):
        raise atscale_errors.UserError(
            f'Dataset \'{dataset_name}\' not associated with given model')

    if not data_model.column_exists(dataset_name, column_name):
        raise atscale_errors.UserError(
            f'Column \'{column_name}\' not found in the \'{dataset_name}\' dataset')

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

    project_json = data_model.project._get_dict()
    uid = str(uuid.uuid4())

    cube = project_parser.get_cube(project_dict=project_json,
                                   id=data_model.cube_id)

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

    data_model.project._update_project(
        project_json=project_json, publish=publish)


def update_aggregate_feature_metadata(data_model: DataModel, feature_name: str, description: str = None, caption: str = None,
                                      folder: str = None,
                                      format_string: Optional[Union[FeatureFormattingType, str]] = None,
                                      visible: bool = None, publish: str = True):
    """Update the metadata for an aggregate feature.

    Args:
        data_model (DataModel): the datamodel object to work with
        feature_name (str): The name of the feature to update.
        description (str): The description for the feature. Defaults to None to leave unchanged.
        caption (str): The caption for the feature. Defaults to None to leave unchanged.
        folder (str): The folder to put the feature in. Defaults to None to leave unchanged.
        format_string (str): The format string for the feature. Defaults to None to leave unchanged.
        visible (bool, optional): Whether or not the feature will be visible to BI tools. Defaults to None to leave unchanged.
        publish (bool): Whether the updated project should be published. Defaults to True.

    Raises:
        atscale_error.UserError: If the given name does not exist in the data model.
    """

    agg_feature_matches = get_dmv_data(data_model, [Measure.type], filter_by={
        Measure.type: ['Aggregate'],
        Measure.name: [feature_name]})

    if not agg_feature_matches:
        raise atscale_errors.UserError(
            f'Invalid name: \'{feature_name}\'. A feature with that name does not exist')

    if isinstance(format_string, FeatureFormattingType):
        formatting = {
            'named-format': format_string.value}
    else:
        formatting = {
            'format-string': format_string}

    if caption == '':
        caption = feature_name

    project_json = data_model.project._get_dict()

    cube = project_parser.get_cube(project_dict=project_json,
                                   id=data_model.cube_id)

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

    data_model.project._update_project(
        project_json=project_json, publish=publish)


def _create_rolling_helper(data_model: DataModel, prefix, new_feature_name, numeric_feature_name, time_length, hierarchy_name,
                           level_name,
                           description, caption, folder, format_string, visible, publish):
    """ Factors out common code from several of the following functions that create calculated features.

    :param DataModel data_model: The AtScale DataModel that the feature will be written into.
    :param str prefix: The prefix to the query specifying what sort of feature is being created.
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
    :param bool publish: Whether or not the updated project should be published.
    """
    check_features([numeric_feature_name], list(data_model.get_features()['name']),
                   errmsg=f'Make sure \'{numeric_feature_name}\' is a numeric feature')

    if not (type(time_length) == int) or time_length < 1:
        raise atscale_errors.UserError(
            f'Invalid parameter value \'{time_length}\', Length must be an integer greater than zero')

    hier_dict, level_dict = _check_time_hierarchy(data_model=data_model, hierarchy_name=hierarchy_name,
                                                  level_name=level_name)

    time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]

    expression = prefix.value + f'(' \
                                f'ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}]' \
                                f', {time_length - 1}, [{time_dimension}].[{hierarchy_name}].CurrentMember)' \
                                f':[{time_dimension}].[{hierarchy_name}].CurrentMember, [Measures].[{numeric_feature_name}])'
    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)
    # todo: use create_calculated_feature_local
    return f'Successfully created measure \'{new_feature_name}\' {f"in folder {folder}" if folder else ""}'


def create_rolling_mean(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str,
                        level_name: str, description: str = None, caption: str = None, folder: str = None,
                        format_string: str = None, visible: bool = True, publish: bool = True) -> str:
    """Creates a rolling mean calculated numeric feature

    Args:
        data_model (DataModel): The AtScale DataModel that the feature will be written into
        new_feature_name (str): What the feature will be called
        numeric_feature_name (str): The numeric feature to use for the calculation
        time_length (int): The length of time the mean should be calculated over
        hierarchy_name (str): The time hierarchy used in the calculation
        level_name (str): The level within the time hierarchy
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Returns:
        str: A message stating that the feature was successfully created
    """
    _create_rolling_helper(data_model=data_model, prefix=MDXAggs.MEAN,
                           new_feature_name=new_feature_name, numeric_feature_name=numeric_feature_name, time_length=time_length, hierarchy_name=hierarchy_name,
                           level_name=level_name, description=description, caption=caption, folder=folder,
                           format_string=format_string, visible=visible, publish=publish)


def create_rolling_sum(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str,
                       level_name: int, description: str = None, caption: str = None, folder: str = None,
                       format_string: str = None, visible: bool = True, publish: bool = True) -> str:
    """Creates a rolling sum calculated numeric feature

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): What the feature will be called
        numeric_feature_name (str): The numeric feature to use for the calculation
        time_length (int): The length of time the sum should be calculated over
        hierarchy_name (str): The time hierarchy used in the calculation
        level_name (str): The level within the time hierarchy
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Returns:
        str: A message stating that the feature was successfully created
    """
    _create_rolling_helper(data_model=data_model, prefix=MDXAggs.SUM,
                           new_feature_name=new_feature_name, numeric_feature_name=numeric_feature_name, time_length=time_length, hierarchy_name=hierarchy_name,
                           level_name=level_name, description=description, caption=caption, folder=folder,
                           format_string=format_string, visible=visible, publish=publish)


def create_rolling_max(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str,
                       level_name: str, description: str = None, caption: str = None, folder: str = None,
                       format_string: str = None, visible: bool = True, publish: bool = True) -> str:
    """Creates a rolling max calculated numeric feature

    Args:
        data_model (DataModel): The AtScale DataModel that the feature will be written into
        new_feature_name (str): What the feature will be called
        numeric_feature_name (str): The numeric feature to use for the calculation
        time_length (int): The length of time the max should be calculated over
        hierarchy_name (str): The time hierarchy used in the calculation
        level_name (str): The level within the time hierarchy
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Returns:
        str: A message stating that the feature was successfully created
    """
    _create_rolling_helper(data_model=data_model, prefix=MDXAggs.MAX,
                           new_feature_name=new_feature_name, numeric_feature_name=numeric_feature_name, time_length=time_length, hierarchy_name=hierarchy_name,
                           level_name=level_name, description=description, caption=caption, folder=folder,
                           format_string=format_string, visible=visible, publish=publish)


def create_rolling_min(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str,
                       level_name: str, description: str = None, caption: str = None, folder: str = None,
                       format_string: str = None, visible: bool = True, publish: bool = True) -> str:
    """Creates a rolling min calculated numeric feature

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): What the feature will be called
        numeric_feature_name (str): The numeric feature to use for the calculation
        time_length (int): The length of time the min should be calculated over
        hierarchy_name (str): The time hierarchy used in the calculation
        level_name (str): The level within the time hierarchy
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Returns:
        str: A message stating that the feature was successfully created
    """
    _create_rolling_helper(data_model=data_model, prefix=MDXAggs.MIN,
                           new_feature_name=new_feature_name, numeric_feature_name=numeric_feature_name, time_length=time_length, hierarchy_name=hierarchy_name,
                           level_name=level_name, description=description, caption=caption, folder=folder,
                           format_string=format_string, visible=visible, publish=publish)


def create_rolling_stdev(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str,
                         level_name: str, description: str = None, caption: str = None, folder: str = None,
                         format_string: str = None, visible: bool = True, publish: bool = True) -> str:
    """Creates a rolling standard deviation calculated numeric feature

    Args:
        data_model (DataModel): The AtScale DataModel that the feature will be written into
        new_feature_name (str): What the feature will be called
        numeric_feature_name (str): The numeric feature to use for the calculation
        time_length (int): The length of time the standard deviation should be calculated over
        hierarchy_name (str): The time hierarchy used in the calculation
        level_name (str): The level within the time hierarchy
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Returns:
        str: A message stating that the feature was successfully created
    """
    _create_rolling_helper(data_model=data_model, prefix=MDXAggs.STANDARD_DEVIATION,
                           new_feature_name=new_feature_name, numeric_feature_name=numeric_feature_name, time_length=time_length, hierarchy_name=hierarchy_name,
                           level_name=level_name, description=description, caption=caption, folder=folder,
                           format_string=format_string, visible=visible, publish=publish)


def create_rolling_stats(data_model: DataModel, numeric_features: List[str], hierarchy_name: str, level_name: str,
                         intervals: Union[int, List[int]] = None, description: str = None, folder: str = None,
                         format_string: str = None, visible: bool = True, publish: bool = True) -> List[str]:
    """Creates a rolling min, max, mean, sum, stddev, and lag of numeric features

    Args:
        data_model (DataModel): The AtScale DataModel that the feature will be written into
        numeric_features (List[str]): The numeric features to use for the calculation
        hierarchy_name (str): The hierarchy that the time level belongs to
        level_name (str): The time level to use for the calculation
        intervals (Union[int, List[int]], optional): Custom list of intervals to create features over. Defaults to None.
        description (str, optional): The description for the features. Defaults to None.
        folder (str, optional): The folder to put the features in. Defaults to None.
        format_string (str, optional): The format string for the features. Defaults to None.
        visible (bool, optional): Whether the features will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: Intervals passed must be positive integers

    Returns:
        List[str]: A list of the new features created
    """
    hier_dict, level_dict = _check_time_hierarchy(data_model=data_model,
                                                  hierarchy_name=hierarchy_name,
                                                  level_name=level_name)

    if type(numeric_features) != list:
        numeric_features = [numeric_features]

    measure_list = list(get_dmv_data(
        model=data_model, id_field=Measure.name).keys())
    check_features(numeric_features, measure_list,
                   errmsg='Invalid parameter: numeric_features. One or more of the given features are not '
                   'existent numeric features in the data model.')

    time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]
    time_numeric = level_dict[level_name][Level.type.name]
    # takes out the Time and 's' at the end and in lowercase
    time_name = str(time_numeric)[4:-1].lower()

    if intervals:
        if type(intervals) != list:
            intervals = [intervals]
    else:
        intervals = TimeSteps[time_numeric].value

    project_json = data_model.project._get_dict()
    name_list = []
    features_to_create: List[tuple] = []  # name, expression, folder
    for feature in numeric_features:
        if folder is None:
            feature_folder = f'{feature}_{time_name}_rolling_stats'
        else:
            feature_folder = folder
        for length in intervals:
            if not (type(length) == int) or length < 1:
                raise atscale_errors.UserError(
                    f'Invalid parameter value \'{length}\', intervals must be an integer greater than zero')
            length = int(length)
            name = f'{feature}_{length}_{time_name}_'
            if length > 1:
                for agg in MDXAggs:
                    specific_name = f'{name}{agg.name.lower()}'
                    expression = agg.value + f'(' \
                                             f'ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}]' \
                                             f', {length - 1}, [{time_dimension}].[{hierarchy_name}].CurrentMember)' \
                                             f':[{time_dimension}].[{hierarchy_name}].CurrentMember, ' \
                                             f'[Measures].[{feature}])'
                    features_to_create.append(
                        (specific_name, expression, feature_folder))
                    name_list.append(specific_name)
            expression = f'(ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}]' \
                         f', {length}, [{time_dimension}].[{hierarchy_name}].CurrentMember)' \
                         f', [Measures].[{feature}])'
            specific_name = f'{name}lag'
            features_to_create.append(
                (specific_name, expression, feature_folder))
            name_list.append(specific_name)
    for specific_name in name_list:
        if specific_name in measure_list:
            raise atscale_errors.UserError(
                f'Invalid name: \'{specific_name}\'. A feature already exists with that name')
    for (specific_name, expression, folder) in features_to_create:
        _create_calculated_feature_local(project_json=project_json,
                                         cube_id=data_model.cube_id,
                                         name=specific_name,
                                         expression=expression,
                                         description=description,
                                         folder=folder,
                                         format_string=format_string,
                                         visible=visible)

    data_model.project._update_project(
        project_json=project_json, publish=publish)
    return name_list


def create_lag(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str, level_name: str,
               description: str = None, caption: str = None, folder: str = None, format_string: str = None, visible: bool = True,
               publish: bool = True):
    """Creates a lagged feature based on the numeric feature and time hierachy passed in.

    Args:
        data_model (DataModel): The data model to build the feature in.
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
    check_features(features=[numeric_feature_name],
                   check_list=list(get_dmv_data(model=data_model, fields=[],
                                                id_field=Measure.name,
                                                filter_by={
                                                    Measure.name: [numeric_feature_name]}).keys()),
                   errmsg=f'Invalid parameter value \'{numeric_feature_name}\' is not a numeric feature in the data model')

    if not (type(time_length) == int) or time_length <= 0:
        raise atscale_errors.UserError(
            f'Invalid parameter value \'{time_length}\', Length must be an integer greater than zero')

    hier_dict, level_dict = _check_time_hierarchy(data_model=data_model, hierarchy_name=hierarchy_name,
                                                  level_name=level_name)

    time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]

    expression = f'(ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}], {time_length}' \
                 f', [{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}])'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_one_hot_encoded_features(data_model: DataModel, categorical_feature: str, description: str = None, folder: str = None,
                                    format_string: str = None, publish: bool = True) -> List[str]:
    """Creates a one hot encoded feature for each value in the given categorical feature

    Args:
        data_model (DataModel): The data model to add the features to.
        categorical_feature (str): The categorical feature to pull the values from.
        description (str, optional): A description to add to the new features. Defaults to None.
        folder (str, optional): The folder to put the new features in. Defaults to None.
        format_string (str, optional): A format sting for the new features. Defaults to None.
        publish (bool, optional): Whether to publish the project after creating the features. Defaults to True.

    Raises:
        atscale_errors.UserError: If the given catagorical feature can't be found
        atscale_errors.UserError: If a feature already exists with the generated name

    Returns:
        List[str]: The names of the newly created features
    """
    level_heritage = get_dmv_data(model=data_model,
                                  fields=[Level.dimension, Level.hierarchy],
                                  filter_by={
                                      Level.name: [categorical_feature]})

    if len(level_heritage) == 0:
        raise atscale_errors.UserError(
            f'Level: {categorical_feature} does not exist in the model')
    dimension = level_heritage[categorical_feature][Level.dimension.name]
    hierarchy = level_heritage[categorical_feature][Level.hierarchy.name]
    df_values = data_model.get_data([categorical_feature])
    project_json = data_model.project._get_dict()
    created_names = []
    for value in df_values[categorical_feature].values:
        expression = f'IIF(ANCESTOR([{dimension}].[{hierarchy}].CurrentMember, [{dimension}].[{hierarchy}].[{categorical_feature}]).MEMBER_NAME="{value}",1,0)'
        name = f'{categorical_feature}_{value}'
        created_names.append(name)
        _create_calculated_feature_local(project_json, data_model.cube_id, name, expression, description=description, caption=None,
                                         folder=folder,
                                         format_string=format_string)

    existing_measures = get_dmv_data(model=data_model,
                                     id_field=Measure.name)
    for name in created_names:
        if name in existing_measures:
            raise atscale_errors.UserError(
                f'Invalid name: \'{name}\'. A feature already exists with that name')
    data_model.project._update_project(
        project_json=project_json, publish=publish)
    return created_names


def create_time_differencing(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, time_length: int,
                             hierarchy_name: str, level_name: str, description: str = None, caption: str = None,
                             folder: str = None, format_string: Optional[Union[str, FeatureFormattingType]] = None,
                             visible: bool = True, publish: bool = True):
    """Creates a time over time subtraction calculation. For example, create_time_differencing on the feature 'revenue'
    , time level 'date', and a length of 2 will create a feature calculating the revenue today subtracted by the revenue
     two days ago

    Args:
        data_model (DataModel): The DataModel that this feature will be written to.
        new_feature_name (str): What the feature will be called.
        numeric_feature_name (str): The numeric feature to use for the calculation.
        length (int): The length of the lag in units of the given level of the given time_hierarchy.
        hierarchy_name (str): The time hierarchy used in the calculation.
        level_name (str): The level within the time hierarchy
        description (str): The description for the feature. Defaults to None.
        caption (str): The caption for the feature. Defaults to None.
        folder (str): The folder to put the feature in. Defaults to None.
        format_string (str): The format string for the feature. Defaults to None.
        publish (bool): Whether or not the updated project should be published. Defaults to True.
    """
    existing_measures = get_dmv_data(model=data_model, fields=[],
                                     id_field=Measure.name)

    check_features(features=[numeric_feature_name],
                   check_list=list(existing_measures.keys()))

    if not (type(time_length) == int) or time_length < 1:
        raise atscale_errors.UserError(
            f'Invalid parameter value \'{time_length}\', Length must be an integer greater than zero')

    hier_dict, level_dict = _check_time_hierarchy(data_model=data_model, hierarchy_name=hierarchy_name,
                                                  level_name=level_name)

    time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]

    expression = f'CASE WHEN IsEmpty((ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}], {time_length}' \
                 f', [{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}])) ' \
                 f'THEN 0 ELSE ([Measures].[{numeric_feature_name}]' \
                 f'-(ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}], {time_length}' \
                 f', [{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}])) END'
    project_json = data_model.project._get_dict()
    if new_feature_name in existing_measures:
        raise atscale_errors.UserError(
            f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')
    _create_calculated_feature_local(project_json=project_json,
                                     cube_id=data_model.cube_id,
                                     name=new_feature_name,
                                     expression=expression,
                                     description=description, caption=caption, folder=folder,
                                     format_string=format_string, visible=visible)
    data_model.project._update_project(
        project_json=project_json, publish=publish)


def create_percentage(data_model: DataModel, numeric_feature_name: str, hierarchy_name: str, level_name: str, new_feature_name: str,
                      description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                      visible: bool = True, publish: bool = True):
    """Creates a feature calculating the percentage of the given numeric_feature's value compared to the given level

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        numeric_feature_name (str): The numeric feature to use for the calculation
        hierarchy_name (str): The hierarchy to use for comparison
        level_name (str): The level of the hierarchy to compare to
        new_feature_name (str): The name of the new feature
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    create_percentages(data_model=data_model, numeric_feature_name=numeric_feature_name, hierarchy_name=hierarchy_name,
                       level_names=[level_name], new_feature_names=[
                           new_feature_name], description=description,
                       caption=caption, folder=folder, format_string=format_string, visible=visible, publish=publish)


def create_percentages(data_model: DataModel, numeric_feature_name: str, hierarchy_name: str,
                       level_names: List[str] = None, new_feature_names: List[str] = None,
                       description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                       visible: bool = True, publish: bool = True):
    """Creates a feature calculating the percentage of the given numeric_feature's value compared to each non-leaf 
       (i.e. non-base) level in the hierarchy

    Args:
        data_model (DataModel): The DataModel to run this operation on
        numeric_feature_name (str): The numeric feature to use for the calculation
        hierarchy_name (str): The hierarchy to use for comparisons
        level_names (List[str], optional): The subset of levels to make percentages for, if None generates 
            percentages for all non-leaf levels. Defaults to None.  
        new_feature_names (List[str], optional): The names of the new columns, if None generates 
            names. If not None it must be same length and order as level_names. Defaults to None.  
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the new features. Defaults to None.
        folder (str, optional): The folder to put the new features in. Defaults to None.
        format_string (str, optional): The format string for the features. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    hier_dict, level_dict = _check_time_hierarchy(
        data_model=data_model, hierarchy_name=hierarchy_name)

    dimension_name = hier_dict[hierarchy_name][Hierarchy.dimension.name]
    level_list = list(get_dmv_data(model=data_model, fields=[Level.name, Level.hierarchy],
                                   filter_by={Level.hierarchy: [hierarchy_name]}).keys())
    measure_list = list(get_dmv_data(
        model=data_model, id_field=Measure.name).keys())

    check_features(features=[numeric_feature_name],
                   check_list=measure_list,  # todo: make this check for draft measures too
                   errmsg=f'Invalid parameter value \'{numeric_feature_name}\' is not a numeric feature in the data model')

    project_dict = data_model.project._get_dict()

    # some error checking on the levels
    if level_names:
        missing_levels = [x for x in level_names if x not in level_list]
        if missing_levels:
            raise atscale_errors.UserError(
                f'Level name{"s" if len(missing_levels) > 1 else ""}: {", ".join(missing_levels)} not found '
                f'in Hierachy: {hierarchy_name}')
        elif level_list[-1] in level_names:
            raise atscale_errors.UserError(
                f'Cannot create percentage for leaf node of hierarchy: {level_list[-1]}')
    else:
        level_names = level_list[:-1]

    if (new_feature_names is not None) and (len(new_feature_names) != len(level_names)):
        raise atscale_errors.UserError(
            f'Length of new_feature_names must equal length of level_names')

    name_list = []
    for lev_index, level in enumerate(level_names):
        if new_feature_names:
            name = new_feature_names[lev_index]
        else:
            name = numeric_feature_name + '% of ' + level
        name_list.append(name)
        _create_percentage_local(project_dict=project_dict, cube_id=data_model.cube_id, name=name,
                                 numeric_feature_name=numeric_feature_name, dimension_name=dimension_name,
                                 hierarchy_name=hierarchy_name, level_name=level, description=description,
                                 caption=caption, folder=folder, format_string=format_string, visible=visible)
    for name in name_list:
        if name in measure_list:
            raise atscale_errors.UserError(
                f'Invalid name: \'{name}\'. A feature already exists with that name')
    data_model.project._update_project(
        project_json=project_dict, publish=publish)


def _create_percentage_local(project_dict, cube_id, name, numeric_feature_name, dimension_name, hierarchy_name, level_name,
                             description=None, caption=None, folder=None, format_string=None, visible=True):
    expression = f'IIF( (Ancestor([{dimension_name}].[{hierarchy_name}].currentMember' \
                 f', [{dimension_name}].[{hierarchy_name}].[{level_name}]), ' \
                 f'[Measures].[{numeric_feature_name}]) = 0, NULL, ' \
                 f'[Measures].[{numeric_feature_name}]' \
                 f' / (Ancestor([{dimension_name}].[{hierarchy_name}].currentMember' \
                 f', [{dimension_name}].[{hierarchy_name}].[{level_name}]), [Measures].[{numeric_feature_name}]))'
    _create_calculated_feature_local(project_json=project_dict, cube_id=cube_id, name=name, expression=expression,
                                     description=description, caption=caption, folder=folder,
                                     format_string=format_string, visible=visible)


def create_percent_change(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, time_length: int, hierarchy_name: str,
                          level_name: str, description: str = None, caption: str = None, folder: str = None,
                          format_string: str = None, visible: bool = True, publish: bool = True):
    """Creates a time over time calculation

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The numeric feature to use for the calculation
        time_length (int): The length of the lag
        hierarchy_name (str): The time hierarchy used in the calculation
        level_name (str): The level within the time hierarchy
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: Given length must be a positive integer
    """
    check_features(features=[numeric_feature_name],
                   check_list=list(get_dmv_data(model=data_model, fields=[],
                                                id_field=Measure.name,
                                                filter_by={
                                                    Measure.name: [numeric_feature_name]}).keys()),
                   errmsg=f'Invalid parameter value \'{numeric_feature_name}\' is not a numeric feature in the data model')

    if not (type(time_length) == int) or time_length <= 0:
        raise atscale_errors.UserError(
            f'Invalid parameter value \'{time_length}\', Length must be an integer greater than zero')

    hier_dict, level_dict = _check_time_hierarchy(data_model=data_model, hierarchy_name=hierarchy_name,
                                                  level_name=level_name)

    time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]

    expression = f'CASE WHEN IsEmpty((ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}], {time_length}' \
                 f', [{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}])) ' \
                 f'THEN 0 ELSE ([Measures].[{numeric_feature_name}]' \
                 f'/(ParallelPeriod([{time_dimension}].[{hierarchy_name}].[{level_name}], {time_length}' \
                 f', [{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}]) - 1) END'
    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_period_to_date(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, hierarchy_name: str, level_name: str,
                          description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                          visible: bool = True, publish: bool = True):
    """Creates a period-to-date calculation

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The numeric feature to use for the calculation
        hierarchy_name (str): The time hierarchy used in the calculation
        level_name (str): The level within the time hierarchy
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    existing_measures = get_dmv_data(model=data_model, fields=[],
                                     id_field=Measure.name)

    check_features(features=[numeric_feature_name],
                   check_list=list(existing_measures.keys()),
                   errmsg=f'Invalid parameter value \'{numeric_feature_name}\' is not a numeric feature in the data model')

    if new_feature_name in existing_measures:
        raise atscale_errors.UserError(
            f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')

    hier_dict, level_dict = _check_time_hierarchy(data_model=data_model, hierarchy_name=hierarchy_name,
                                                  level_name=level_name)

    time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]

    expression = f'CASE WHEN IsEmpty([Measures].[{numeric_feature_name}]) THEN NULL ELSE ' \
                 f'Sum(PeriodsToDate([{time_dimension}].[{hierarchy_name}].[{level_name}], ' \
                 f'[{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}]) END'

    project_json = data_model.project._get_dict()
    cube_id = data_model.cube_id
    _create_calculated_feature_local(project_json, cube_id, new_feature_name, expression, description=description, caption=caption,
                                     folder=folder, format_string=format_string, visible=visible)
    data_model.project._update_project(
        project_json=project_json, publish=publish)


def create_pct_error_calculation(data_model: DataModel, new_feature_name: str, predicted_feature_name: str, actual_feature_name: str,
                                 description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                                 visible: bool = True, publish: bool = True):
    """Creates a calculation for the percent error of a predictive feature compared to the actual feature

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        predicted_feature_name (str): The name of the feature containing predictions
        actual_feature_name (str): The name of the feature to compare the predictions to
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    features_df = data_model.get_features()
    numerics = [features_df['name'][i] for i in features_df.index if
                features_df['data type'][i] == 'Aggregate' or features_df['data type'][i] == 'Calculated']
    check_features([predicted_feature_name], numerics,
                   f"Make sure '{predicted_feature_name}' is a numeric feature")
    check_features([actual_feature_name], numerics,
                   f"Make sure '{actual_feature_name}' is a numeric feature")

    expression = f'100*([Measures].[{predicted_feature_name}] - [Measures].[{actual_feature_name}]) / ' \
                 f'[Measures].[{actual_feature_name}]'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_scaled_feature_minmax(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, min: float, max: float, feature_min: float = 0,
                                 feature_max: float = 1, description: str = None, caption: str = None, folder: str = None,
                                 format_string: str = None, visible: bool = True, publish: bool = True):
    """Creates a new feature that is minmax scaled

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The name of the feature to scale
        min (float): The min from the base feature
        max (float): The max from the base feature
        feature_min (float, optional): The min for the scaled feature. Defaults to 0.
        feature_max (float, optional): The max for the scaled feature. Defaults to 1.
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    expression = f'(([Measures].[{numeric_feature_name}] - {min})/({max}-{min}))' \
                 f'*({feature_max}-{feature_min})+{feature_min}'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_scaled_feature_z_score(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, mean: float = 0, standard_deviation: float = 1,
                                  description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                                  visible: bool = True, publish: bool = True):
    """Creates a new feature that is standard scaled

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The name of the feature to scale
        mean (float, optional): The mean from the base feature. Defaults to 0.
        standard_deviation (float, optional): The standard deviation from the base feature. Defaults to 1.
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    expression = f'([Measures].[{numeric_feature_name}] - {mean}) / {standard_deviation}'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_scaled_feature_maxabs(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, maxabs: float, description: str = None, caption: str = None,
                                 folder: str = None, format_string: str = None, visible: bool = True, publish: bool = True):
    """Creates a new feature that is maxabs scaled

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The name of the feature to scale
        maxabs (float): The max absolute value of any data point from the base feature
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    maxabs = abs(maxabs)
    expression = f'[Measures].[{numeric_feature_name}] / {maxabs}'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_scaled_feature_robust(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, median: float = 0, interquartile_range: float = 1,
                                 description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                                 visible: bool = True, publish: bool = True):
    """Creates a new feature that is robust scaled; mirrors default behavior of sklearn.preprocessing.RobustScaler

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The name of the feature to scale
        median (float, optional): _description_. Defaults to 0.
        interquartile_range (float, optional): _description_. Defaults to 1.
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    expression = f'([Measures].[{numeric_feature_name}] - {median}) / {interquartile_range}'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_scaled_feature_log_transformed(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, description: str = None, caption: str = None,
                                          folder: str = None, format_string: str = None, visible: bool = True, publish: bool = True):
    """Creates a new feature that is log transformed

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The name of the feature to scale
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    expression = f'log([Measures].[{numeric_feature_name}])'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_scaled_feature_unit_vector_norm(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, magnitude: float, description: str = None,
                                           caption: str = None, folder: str = None, format_string: str = None, visible: bool = True,
                                           publish: bool = True):
    """Creates a new feature that is unit vector normalized

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The name of the feature to scale
        magnitude (float): The magnitude of the base feature, i.e. the square root of the sum of the squares of numeric_feature's data points
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    expression = f'[Measures].[{numeric_feature_name}]/{magnitude}'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_scaled_feature_power_transformed(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, power: float, method: str = 'yeo-johnson',
                                            description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                                            visible: bool = True, publish: bool = True):
    """Creates a new feature that is power transformed

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The name of the feature to scale
        power (float): The exponent used in the scaling
        method (str, optional): Which power transformation method to use. Defaults to 'yeo-johnson'.
        description (str, optional): The description for the feature. Defaults to None. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Raises:
        atscale_errors.UserError: User must pass either of two valid power transformation methods
    """
    if method.lower() == 'yeo-johnson':
        if power == 0:
            expression = f'IIF([Measures].[{numeric_feature_name}]<0,' \
                f'(-1*((((-1*[Measures].[{numeric_feature_name}])+1)^(2-{power}))-1))' \
                f'/(2-{power}),log([Measures].[{numeric_feature_name}]+1))'
        elif power == 2:
            expression = f'IIF([Measures].[{numeric_feature_name}]<0,' \
                f'(-1*log((-1*[Measures].[{numeric_feature_name}])+1)),' \
                f'((([Measures].[{numeric_feature_name}]+1)^{power})-1)/{power})'
        else:
            expression = f'IIF([Measures].[{numeric_feature_name}]<0,' \
                f'(-1*((((-1*[Measures].[{numeric_feature_name}])+1)^(2-{power}))-1))/(2-{power}),' \
                f'((([Measures].[{numeric_feature_name}]+1)^{power})-1)/{power})'
    elif method.lower() == 'box-cox':
        if power == 0:
            expression = f'log([Measures].[{numeric_feature_name}])'
        else:
            expression = f'(([Measures].[{numeric_feature_name}]^{power})-1)/{power}'
    else:
        raise atscale_errors.UserError(
            'Invalid type: Valid values are yeo-johnson and box-cox')

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)


def create_periods_to_date(data_model: DataModel, numeric_feature_name: str, hierarchy_name: str, description: str = None,
                           folder: str = None, format_string: str = None, visible: bool = True,
                           publish: bool = True) -> str:
    """Creates a period-to-date calculation

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        numeric_feature_name (str): The numeric feature to use for the calculation
        hierarchy_name (str): The time hierarchy used in the calculation
        description (str, optional): The description for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.

    Returns:
        str: A message containing the names of successfully created features
    """
    hier_dict, level_dict = _check_time_hierarchy(
        data_model=data_model, hierarchy_name=hierarchy_name)
    level_dict = get_dmv_data(model=data_model, fields=[lev for lev in Level])

    hier_levels = []
    time_dimension = hier_dict[hierarchy_name][Hierarchy.dimension.name]
    for l in level_dict.values():
        if l[Level.hierarchy.name] == hierarchy_name:
            hier_levels.append(l)
    # sort so output or error is in order
    hier_levels = sorted(hier_levels, key=(
        lambda x: x[Level.level_number.name]), reverse=False)
    base = hier_levels[-1]

    existing_measures = list(get_dmv_data(
        model=data_model, id_field=Measure.name).keys())
    check_features(features=[numeric_feature_name],
                   check_list=existing_measures)

    project_json = data_model.project._get_dict()
    cube_id = data_model.cube_id
    names = []
    for level in hier_levels[:-1]:
        names.append(
            f'{numeric_feature_name}_{level[Level.name.name]}_To_{base[Level.name.name]}')
        level_name = level[Level.name.name]
        true_description = f'A sum of {numeric_feature_name} from all {base[Level.name.name]} entries in the past ' \
                           f'{level_name}. \n {description if description else ""}'
        expression = f'CASE WHEN IsEmpty([Measures].[{numeric_feature_name}]) THEN NULL ELSE ' \
                     f'Sum(PeriodsToDate([{time_dimension}].[{hierarchy_name}].[{level_name}], ' \
                     f'[{time_dimension}].[{hierarchy_name}].CurrentMember), [Measures].[{numeric_feature_name}]) END'
        _create_calculated_feature_local(project_json=project_json, cube_id=cube_id, name=names[-1],
                                         expression=expression, description=true_description, caption=None,
                                         folder=folder, format_string=format_string, visible=visible)
    for name in names:
        if name in existing_measures:
            raise atscale_errors.UserError(
                f'Invalid name: \'{name}\'. A feature already exists with that name')
    data_model.project._update_project(
        project_json=project_json, publish=publish)
    return f'Successfully created measures {", ".join(names)}'


def create_net_error_calculation(data_model: DataModel, new_feature_name: str, predicted_feature_name: str, actual_feature_name: str,
                                 description: str = None, caption: str = None, folder: str = None, format_string: str = None,
                                 visible: bool = True, publish: bool = True):
    """Creates a calculation for the net error of a predictive feature compared to the actual feature

    Args:
        data_model (DataModel): The Data Model that the feature will be created in
        new_feature_name (str): What the feature will be called
        predicted_feature_name (str): The name of the feature containing predictions
        actual_feature_name (str): The name of the feature to compare the predictions to
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the created feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    measure_list = list(get_dmv_data(model=data_model,
                                     id_field=Measure.name,
                                     filter_by={Measure.name: [predicted_feature_name, actual_feature_name]}).keys())
    check_features([predicted_feature_name], measure_list,
                   f'Invalid parameter value \'{predicted_feature_name}\' '
                   f'is not a numeric feature in the data model')
    check_features([actual_feature_name], measure_list,
                   f'Invalid parameter value \'{actual_feature_name}\' '
                   f'is not a numeric feature in the data model')
    level_list = list(get_dmv_data(model=data_model, id_field=Level.name,
                                   filter_by={Level.name: [new_feature_name]}).keys())
    feature_list = measure_list + level_list

    if new_feature_name in feature_list:
        raise atscale_errors.UserError(
            f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')

    project_dict = data_model.project._get_dict()
    expression = f'[Measures].[{predicted_feature_name}] - [Measures].[{actual_feature_name}]'
    _create_calculated_feature_local(project_json=project_dict,
                                     cube_id=data_model.cube_id,
                                     name=new_feature_name,
                                     expression=expression,
                                     description=description,
                                     caption=caption,
                                     folder=folder,
                                     format_string=format_string,
                                     visible=visible)
    data_model.project._update_project(
        project_json=project_dict, publish=publish)


def create_binned_feature(data_model: DataModel, new_feature_name: str, numeric_feature_name: str, bin_edges: List[float], description: str = None,
                          caption: str = None, folder: str = None, format_string: str = None, visible: bool = True,
                          publish: bool = True):
    """Creates a new feature that is binned

    Args:
        data_model (DataModel): The DataModel that the feature will be written into
        new_feature_name (str): The name of the new feature
        numeric_feature_name (str): The name of the feature to bin
        bin_edges (List[float]): The edges to use to compute the bins, left inclusive. Contents of bin_edges are interpreted
                                 in ascending order
        description (str, optional): The description for the feature. Defaults to None.
        caption (str, optional): The caption for the feature. Defaults to None.
        folder (str, optional): The folder to put the feature in. Defaults to None.
        format_string (str, optional): The format string for the feature. Defaults to None.
        visible (bool, optional): Whether the created feature will be visible to BI tools. Defaults to True.
        publish (bool, optional): Whether or not the updated project should be published. Defaults to True.
    """
    bin_edges = sorted(bin_edges)
    expression = f'CASE [Measures].[{numeric_feature_name}]'
    bin = 0
    for edge in bin_edges:
        expression += f' WHEN [Measures].[{numeric_feature_name}] < {edge} THEN {bin}'
        bin += 1
    expression += f' ELSE {bin} END'

    create_calculated_feature(data_model, new_feature_name, expression, description=description, caption=caption, folder=folder,
                              format_string=format_string, visible=visible, publish=publish)
