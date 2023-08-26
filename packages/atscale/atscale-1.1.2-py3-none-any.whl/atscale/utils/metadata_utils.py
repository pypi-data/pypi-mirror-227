from pandas import DataFrame
from typing import List

from atscale.atscale_errors import UserError
from atscale.data_model import DataModel
from atscale.utils.dmv_utils import get_dmv_data
from atscale.utils.enums import Measure, Level, Hierarchy, FeatureType


def get_hierarchies(data_model: DataModel) -> DataFrame:
    """Gets a DataFrame listing a model's hierarchies with columns for name, dimension, and description.
    Secondary attributes are treated as their own hierarchies.

    Args:
        data_model (DataModel): The DataModel object to search through

    Returns:
        DataFrame: A pandas DataFrame containing hierarchy names, dimensions, and descriptions
    """
    hierarchy_dict = get_dmv_data(
        model=data_model,
        fields=[Hierarchy.dimension, Hierarchy.description]
        )

    to_df_list = [[
        hierarchy,
        hierarchy_dict[hierarchy]['dimension'],
        hierarchy_dict[hierarchy]['description']
        ] for hierarchy in hierarchy_dict]

    return DataFrame(to_df_list, columns=['name', 'dimension', 'description'])


def get_hierarchy_levels(data_model: DataModel, hierarchy_name: str) -> DataFrame:
    """Gets a DataFrame listing the levels of a given hierarchy

    Args:
        data_model (str): The DataModel object the given hierarchy exists within.
        hierarchy_name (str): The name of the hierarchy

    Returns:
        DataFrame: A pandas DataFrame containing the hierarchy's levels
    """

    levels_from_hierarchy = get_dmv_data(model=data_model,
                                         fields=[Level.name],
                                         id_field=Level.hierarchy,
                                         filter_by={
                                             Level.hierarchy: [hierarchy_name]})

    hierarhy_names = levels_from_hierarchy.get(hierarchy_name, [])
    return DataFrame([_l.get(Level.name.name) for _l in hierarhy_names],
                     columns=[f'levels of {hierarchy_name}'])


def get_feature_description(data_model: DataModel, feature: str) -> str:
    """Returns the description of a given feature given the DataModel containing it.

    Args:
        data_model (DataModel): The DataModel object the given feature exists within.
        feature (str): The query name of the feature to retrieve the description of.

    Returns:
        str: The description of the given feature.
    """
    return data_model.get_features(feature_list=[feature])['description'][0]


def get_feature_expression(data_model: DataModel, feature: str) -> str:
    """Returns the expression of a given feature given the DataModel containing it.

    Args:
        data_model (DataModel): The DataModel object the given feature exists in.
        feature (str): The query name of the feature to return the expression of.

    Returns:
        str: The expression of the given feature.
    """
    return data_model.get_features(feature_list=[feature])['expression'][0]


def list_all_numeric_features(data_model: DataModel, folder: str = None) -> List[str]:
    """Returns a list of all numeric features (ie Aggregate and Calculated Measures) in a given data model.

    Args:
        data_model (DataModel): The DataModel object to be queried.
        folder (str, optional): The name of a folder in the data model containing measures to exclusively list.
            Defaults to None to not filter by folder.

    Returns:
        List[str]: A list of the query names of numeric features in the data model and, if given, in the folder.
    """
    folders = [folder] if folder else None
    return list(data_model.get_features(folder_list=folders, feature_type=FeatureType.NUMERIC)['name'])


def list_all_categorical_features(data_model: DataModel, folder: str = None) -> List[str]:
    """Returns a list of all categorical features (ie Hierarchy levels and secondary_attributes) in a given DataModel.

    Args:
        data_model (DataModel): The DataModel object to be queried.
        folder (str, optional): The name of a folder in the DataModel containing features to exclusively list.
            Defaults to None to not filter by folder.

    Returns:
        List[str]: A list of the query names of categorical features in the DataModel and, if given, in the folder.
    """
    folders = [folder] if folder else None
    return list(data_model.get_features(folder_list=folders, feature_type=FeatureType.CATEGORICAL)['name'])


def get_folders(data_model: DataModel) -> DataFrame:
    """Returns a DataFrame with a single column for the name of a folder in a given DataModel and rows for each folder.

    Args:
        data_model: The DataModel object to be queried.

    Returns:
        DataFrame: The pandas DataFrame containing a single column 'folders'
    """

    measure_dict = get_dmv_data(
        model=data_model,
        fields=[Measure.folder]
        )

    hierarchy_dict = get_dmv_data(
        model=data_model,
        fields=[Hierarchy.folder]
        )

    to_df_list = sorted(set([measure_dict[key]['folder'] for key in measure_dict.keys()] + \
                            [hierarchy_dict[key]['folder'] for key in hierarchy_dict.keys()]))

    return DataFrame(to_df_list, columns=['folders'])


def _get_hierarchy_level_time_step(data_model: DataModel, hierarchy_name: str, level_name: str):
    """ Gets the time step of a given level

    :param Connection atconn: The Connection object corresponding to the project and model that the hierarchy
                                     and level belong to
    :param str project_name: The name of the project
    :param str model_name: The name of the model
    :param str hierarchy_name: The name of the hierarchy containing the level
    :param str level_name: The name of the level
    :return: The level's time step
    :rtype: str
    """

    hierarchy_dict = get_dmv_data(
        model=data_model,
        fields=[Hierarchy.type],
        filter_by={
            Hierarchy.name: [hierarchy_name]}
        )

    dimension_dict = get_dmv_data(
        model=data_model,
        fields=[Level.type, Level.hierarchy],
        filter_by={
            Level.name: [level_name]}
        )

    hierarchy = hierarchy_dict.get(hierarchy_name)
    level = dimension_dict.get(level_name)

    if hierarchy is None:
        raise UserError(f'Hierarchy: {hierarchy_name} does not exist in the model')
    if level is None:
        raise UserError(f'Level: {level_name} does not exist in the model')
    if level.get(Level.hierarchy.name) != hierarchy_name:
        raise UserError(f'Level: {level_name} does not exist in Hierarchy: {hierarchy_name}')
    if hierarchy.get(Hierarchy.type.name) != 'Time':
        raise UserError(f'Level: {level_name} does not exist in a time hierarchy')

    return level.get('type')


def _hierarchy_dimension(data_model: DataModel, hierarchy_name: str):
    hier_to_dim = get_dmv_data(model=data_model, fields=[Hierarchy.dimension], id_field=Hierarchy.name,
                               filter_by={
                                   Hierarchy.name: [hierarchy_name]})
    if hier_to_dim:
        return hier_to_dim[hierarchy_name][Hierarchy.dimension.name]
    else:
        raise UserError(f'Hierarchy: {hierarchy_name} does not exist in the model')
