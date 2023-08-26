import logging

from atscale.parsers import project_parser

logger = logging.getLogger(__name__)


def _get_cube_datasets(cube_dict: dict):
    """ 
    Retrieves the list of datasets in the cube. Each dataset will be a dict  with information about columns and attached measures.
    Args:
        cube_dict : Dictionary argument that passes in the cube.
    Returns:
        list : List of Dictionaries of datasets in the cube. 
    """
    ds_dict = cube_dict.get('data-sets')
    if ds_dict is None:
        return None
    data_set_ref = ds_dict.get('data-set-ref')
    if data_set_ref is None:
        return []
    return data_set_ref


def get_project_datasets_referenced_by_cube(project_dict: dict, cube_dict: dict) -> list:
    cube_datasets = _get_cube_datasets(cube_dict)
    project_datasets = project_parser.get_datasets(project_dict)
    project_datasets_used_by_cube = []
    for cube_dataset in cube_datasets:
        project_dataset_id_ref = cube_dataset.get('id')
        project_dataset = project_parser.get_dataset_from_datasets(project_datasets, project_dataset_id_ref)
        # if the cube references a dataset that is not in the project then something is wrong
        if project_dataset is None:
            msg = "Data model references dataset that does not exist in the associated project."
            logger.exception(msg)
            raise Exception(msg)
        project_datasets_used_by_cube.append(project_dataset)
    return project_datasets_used_by_cube


def attributes_derived_from_ds(cube: dict, dataset: dict):
    """find attributes in the cube that are created based on a column in the given dataset THAT IS IN THE CUBE"""
    derived_features = []
    derived_attribute_id_to_name: dict[str, str] = {}
    for att in cube['attributes']['attribute']:
        derived_attribute_id_to_name[att['id']] = att['name']
    for att in dataset['logical']['attribute-ref']:
        if att['id'] in derived_attribute_id_to_name:
            derived_features.append(
                derived_attribute_id_to_name[att['id']])
    return derived_features
