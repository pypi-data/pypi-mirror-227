import logging
from typing import Dict, List

from atscale.parsers import project_parser

logger = logging.getLogger(__name__)


def _get_cube_datasets(cube_dict: dict) -> List[Dict]:
    """ 
    Retrieves the list of datasets in the cube. Each dataset will be a dict  with information about columns and attached measures.
    Args:
        cube_dict : Dictionary argument that passes in the cube.
    Returns:
        list : List of Dictionaries of datasets in the cube. 
    """
    if cube_dict is None:
        return []
    ds_dict = cube_dict.get('data-sets', {})
    return ds_dict.get('data-set-ref', [])

def get_data_set_ref(data_model_dict:dict, dataset_id:str)->dict:
    return [x for x in data_model_dict['data-sets']
                    ['data-set-ref'] if x['id'] == dataset_id][0] #careful calling methods, that last index into 0 delists the data-set-ref which is actually a list

def _get_calculated_member_refs(cube_dict: dict) -> List[Dict]  :
    """Grabs the calculated members out of a cube dict. 

    Args:
        cube_dict (dict): a dict describing a calculated members

    Returns:
        list: list of dictionaries describing the calculated member references
    """
    if cube_dict is None:
        return []
    mem_dict = cube_dict.setdefault('calculated-members', {})
    return mem_dict.setdefault('calculated-member-ref', [])


def get_project_datasets_referenced_by_cube(project_dict: dict, cube_dict: dict) -> List:
    cube_datasets = _get_cube_datasets(cube_dict)
    project_datasets = project_parser.get_datasets(project_dict)
    project_datasets_used_by_cube = []
    for cube_dataset in cube_datasets:
        project_dataset_id_ref = cube_dataset.get('id')
        project_dataset = project_parser.get_dataset_from_datasets(project_datasets, project_dataset_id_ref)
        # if the cube references a dataset that is not in the project then something is wrong
        if not project_dataset:
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
    for att in dataset['logical'].get('attribute-ref', []):
        if att['id'] in derived_attribute_id_to_name:
            derived_features.append(
                derived_attribute_id_to_name[att['id']])
    return derived_features
