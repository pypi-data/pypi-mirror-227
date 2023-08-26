import uuid

from atscale.parsers import data_model_parser, project_parser
from atscale.base import templates

def create_measure(project_dict: dict, data_model_id: str, dataset_id: str, column_name: str, 
                   measure_name:str = None, folder:str = None):
    """Mutates the provided project_dict to add a measure in the data_model referenced by model_id. NOTE: this does not update the project. 

    Args:
        project_dict (dict): project dict to be mutated
        data_model_id (str): the id for the data_model to add the measure to
        dataset_id (str): the dataset_id that will be required for the measure
        column_name (str): the name of the column to be used for the measure. 
        measure_name (str, optional): the name of the measure. Defaults to column_name if None 
        folder (str, optional): the folder of the measure. Defaults to None 

    """
    if measure_name is None:
        measure_name = column_name
    # we'll grab the data_model where most of the changes will occur, we don't want a perspective
    data_model_dict = project_parser.get_cube(
        project_dict=project_dict, id=data_model_id)
    data_model_dict.setdefault('attributes', {}) #only has effect if attributes doesn't exist

    #create attribute 
    attribute_id = str(uuid.uuid4())     #This will be used in the attribute entry and referenced in the data-set-ref by an attribute-ref
    attribute_dict = templates.create_attribute_dict_for_measure(attribute_id=attribute_id, name=measure_name, folder=folder)
    data_model_dict['attributes'].setdefault('attribute', []) 
    data_model_dict['attributes']['attribute'].append(attribute_dict)

    #now we add the attribute-ref in data-set-ref
    # grab the data_set_ref in the data_model that references the dataset in the project
    data_set_ref = data_model_parser.get_data_set_ref(
        data_model_dict=data_model_dict, dataset_id=dataset_id)

    attribute_ref_dict = templates.create_attribute_ref_dict(
        columns=[column_name], attribute_id=attribute_id)
    data_set_ref['logical'].setdefault('attribute-ref', [])
    data_set_ref['logical']['attribute-ref'].append(attribute_ref_dict)
