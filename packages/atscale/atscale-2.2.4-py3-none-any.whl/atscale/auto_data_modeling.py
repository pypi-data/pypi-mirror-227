import logging
from atscale.base import templates
from atscale.connection.connection import Connection
from atscale.db.sql_connection import SQLConnection
from atscale.parsers import project_parser
from atscale.utils import dimension_utils, measure_utils, time_utils
from atscale.base.enums import AtScaleColumnTypes

logger = logging.getLogger(__name__)

def create_semantic_layer(atconn: Connection, dbconn: SQLConnection, table_name: str, project_dict: dict, data_model_id: str, dataset_id: str, columns: list):
    """Mutates the provided project_dict to add a semantic layer. NOTE: This does not update the project! Calling methods must still update and publish the project using the resulting project_dict. 

    Args:
        atconn (Connection): AtScale connection
        dbconn (Connection): DB connection
        table_name (str): the name of the table to create a semantic table for
        project_dict (dict): the project dictionary (generally sparse result of creating a new project and adding a dataset)
        data_model_id (str): the id for the data_model (generally sparse result of creating a new project)
        dataset_id (str): the id for the dataset associated with the table_name for which we will create a semantic layer
        columns (list): columns of the table associated with table_name and dataset_id as AtScale sees them, generally with a name and type for each
    """
    for column in columns:
        column_name = column[0]
        # this does a string comparison to see if this column type is a DateTime
        if AtScaleColumnTypes.DateTime.value in column[1] or AtScaleColumnTypes.Date.value in column[1]:
            # Add a dimension for the date column
            try:#determine_time_levels depends on count(distinct(column_name)) sql working. If the db errors out, then we just skip
                time_levels = time_utils.determine_time_levels(
                    dbconn=dbconn, table_name=table_name, column=column_name)
            except Exception as e:
                logger.error(f"Unable to determine TimeLevels in create_semantic_layer for column {column} and db type {dbconn.platform_type}. The error was{e}")
                #skip the rest and go to the next column in the loop
                continue 
            dimension_utils.create_time_dimension_for_column(
                atconn=atconn, project_dict=project_dict, data_model_id=data_model_id, dataset_id=dataset_id, column_name=column_name, time_levels=time_levels)

        elif AtScaleColumnTypes.String.value in column[1]:
            dimension_utils.create_categorical_dimension_for_column(
                atconn=atconn, project_dict=project_dict, data_model_id=data_model_id, dataset_id=dataset_id, column_name=column_name)

        # could pile on the various numeric types, not sure how AtScale sees them all, so far I've seen "Decimal" a lot.
        elif AtScaleColumnTypes.Decimal.value in column[1]:
            # Note that calculated columns pulling out parts of dates will show up as Decimal data type also.
            measure_utils.create_measure(
                project_dict=project_dict, data_model_id=data_model_id, dataset_id=dataset_id, column_name=column_name)

    # The default data_model object when creating a project and writing a dataframe only has a data-set-ref. If we added dimensions above,
    # then we need to add some other dict elements to the data_model. I'm not actually sure how these are used. Just going with some defaults here
    data_model_dict = project_parser.get_cube(
        project_dict=project_dict, id=data_model_id)
    data_model_dict.setdefault(
        'properties', templates.create_data_model_properties_dict_default())
    data_model_dict.setdefault(
        'actions', templates.create_data_model_actions_dict_default())
    # this being empty seems weird since we have calculated columns, but maybe this refers to calculated measures?
    data_model_dict.setdefault('calculated-members', {})
    data_model_dict.setdefault('aggregates', {})


