from typing import List, Dict

from atscale.errors import atscale_errors
from atscale.base import enums
from atscale.data_model.data_model import DataModel
from atscale.parsers import project_parser
from atscale.utils import query_utils, dmv_utils

def write_udf_to_qds(data_model: DataModel,
                     udf_name: str,
                     new_feature_name: str,
                     feature_inputs: List[str]):
    """ Writes a single column output of a udf into the given data_model as a feature. For example, if a
     udf created in snowpark 'udf' outputs predictions based on a given set of features '[f]', then calling
     write_udf_as_qds(data_model=atmodel, udf_name=udf, new_feature_name='predictions' feature_inputs=f)
     will create a new feature called 'predictions' which can be included in any query that excludes categorical features
     that are not accounted for in '[f]' (no feature not in same dimension at same level or lower in [f]). Currently only
     supports snowflake udfs.
    Args:
        data_model (DataModel): The AtScale data model to create the new feature in
        udf_name (str): The name of an existing udf which outputs a single column for every row of input.
            The full name space should be passed (ex. '"DB"."SCHEMA".udf_name').
        new_feature_name (str): The name of the newly created feature from the output of the udf.
        feature_inputs (List[str]): The names of features in data_model that are the inputs for the udf, in the order
            they are passed to the udf.
    Raises:
        atscale_errors.UserError: When new_feature_name already exists as a feature in the given data_model, or any
        feature in feature_inputs does not exist in the given data_model.
        """
    feat_dict: dict = data_model.get_features()
    if new_feature_name in feat_dict.keys():
        raise atscale_errors.UserError(
            f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')
    atscale_query: str = query_utils._generate_atscale_query(data_model=data_model, feature_list=feature_inputs)
    feature_query: str = query_utils.generate_db_query(data_model=data_model,
                                                       atscale_query=atscale_query,
                                                       use_aggs=False)
    categorical_inputs: List[str] = [feat for feat in feature_inputs if feat_dict[feat]['feature type'] == 'Categorical']
    categorical_string: str = ", ".join(f'"{cat}"' for cat in categorical_inputs)
    qds_query: str = f'SELECT {_snowpark_udf_call(udf_name=udf_name, feature_inputs=feature_inputs)} ' \
                     f'as "{new_feature_name}", {categorical_string} FROM ({feature_query})'
    warehouse_id: str = project_parser.get_project_warehouse(project_dict=data_model.project._get_dict())
    data_model.add_queried_dataset(warehouse_id=warehouse_id,
                                   dataset_name=f'{new_feature_name}_QDS',
                                   query=qds_query,
                                   join_features=categorical_inputs)
    data_model.create_aggregate_feature(column_name=new_feature_name,
                                           dataset_name=f'{new_feature_name}_QDS',
                                           name=new_feature_name,
                                           aggregation_type=enums.Aggs.SUM,  # could parameterize
                                           )

def write_linear_regression_model(data_model: DataModel,
                                  model,
                                  new_feature_name: str,
                                  granularity_levels: List[str] = None,
                                  feature_inputs: List[str] = None):
    """ Writes a sklearn LinearRegression model, which takes AtScale features exclusively as input, to the given
    DataModel as a sum aggregated feature with the given name. The feature will return the output of the coefficients
    and intercept in the model applied to feature_inputs as defined in atscale. Omitting feature_inputs will use the
    names of the columns inputted at training time and error if any names are not in the data model.
    Args:
        data_model (DataModel): The AtScale DataModel to add the regression into. 
        model (LinearRegression): The sklearn LinearRegression model to build into a feature.
        new_feature_name (str): The name of the created feature.
        granularity_levels (List[str], optional): List of lowest categorical levels that predictions with this
            model can be run on. Defaults to False to use the lowest level from each hierarchy.
        feature_inputs (List[str], optional): List of names of inputs features in the input order.
            Defaults to None to use the column names used when training the model.
    Raises:
        atscale_errors.UserError: If any of the features in feature inputs do not exist in the data model or if
            there is already a feature with the name new_feature_name
    """
    try:
        from sklearn.linear_model import LinearRegression
    except ImportError:
        raise ImportError('sklearn needs to be installed to use this functionality, the function takes an '
                          'sklearn.linear_model.LinearRegression object. Try running pip install sklearn')
    if not isinstance(model, LinearRegression):
        raise atscale_errors.UserError(f'The model object of type: {type(model)} is not compatible with this method '
                                       f'which takes an object of type sklearn.linear_regression.LinearRegression')
    if new_feature_name in data_model.get_features().keys():
        raise atscale_errors.UserError(
            f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')

    if granularity_levels is None:
        hierarchy_to_levels: Dict['str', List[dict]] = dmv_utils.get_dmv_data(model=data_model,
                                                                          id_field=enums.Level.hierarchy,
                                                                          fields=[enums.Level.name,
                                                                                  enums.Level.level_number])
        leaf_levels: List[str] = []
        for levels in hierarchy_to_levels.values():
            leaf_levels.append(levels[-1]['name'])
        granularity_levels = leaf_levels

    if feature_inputs is None:
        feature_inputs = list(model.feature_names_in_)

    atscale_query: str = query_utils._generate_atscale_query(data_model=data_model,
                                                            feature_list=feature_inputs + granularity_levels)
    feature_query: str = query_utils.generate_db_query(data_model=data_model,
                                                       atscale_query=atscale_query,
                                                       use_aggs=False)
    categorical_string: str = ", ".join(f'"{cat}"' for cat in granularity_levels)
    numeric = ' + '.join([f'{theta1}*"{x}"' for theta1, x in zip(model.coef_[0], model.feature_names_in_)])
    numeric += f' + {model.intercept_[0]}'
    qds_query: str = f'SELECT ({numeric}) as "{new_feature_name}" , {categorical_string} FROM ({feature_query})'
    warehouse_id: str = project_parser.get_project_warehouse(project_dict=data_model.project._get_dict())
    data_model.add_queried_dataset(warehouse_id=warehouse_id,
                                   dataset_name=f'{new_feature_name}_QDS',
                                   query=qds_query,
                                   join_features=granularity_levels)
    data_model.create_aggregate_feature(
                                           column_name=new_feature_name,
                                           dataset_name=f'{new_feature_name}_QDS',
                                           name=new_feature_name,
                                           aggregation_type=enums.Aggs.SUM,  # could parameterize
                                           )

def _snowpark_udf_call(udf_name: str, feature_inputs: List[str]):
    inputs = ", ".join(f'"{f}"' for f in feature_inputs)
    return f'{udf_name}(array_construct({inputs}))'