import uuid
from typing import List, Dict, Union, Tuple

from atscale.errors import atscale_errors
from atscale.base import enums
from atscale.data_model.data_model import DataModel
from atscale.parsers import project_parser
from atscale.db.sql_connection import SQLConnection
from atscale.utils import query_utils, dmv_utils, model_utils, db_utils
from math import e
from atscale.base.enums import Aggs


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
    model_utils._perspective_check(data_model)

    feat_dict: dict = data_model.get_features()
    if new_feature_name in feat_dict.keys():
        raise atscale_errors.UserError(
            f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')
    atscale_query: str = query_utils._generate_atscale_query(data_model=data_model, feature_list=feature_inputs)
    feature_query: str = query_utils.generate_db_query(data_model=data_model,
                                                       atscale_query=atscale_query,
                                                       use_aggs=False)
    categorical_inputs: List[str] = [feat for feat in feature_inputs if feat_dict[feat]['feature_type'] == 'Categorical']
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

def join_udf(data_model: DataModel,
             target_columns: List[str],
             udf_call: str,
             join_columns: List[str] = None,
             join_features: List[str] = None,
             folder: str = None,
             qds_name: str = None,
             warehouse_id: str = None,
             publish: bool = True):
    """ Creates measures for each column in target_columns using the name that they are presented. For example,
    target_columns=['\"predicted_sales\" as \"sales_prediction\"', '\"confidence\"'] would make two measures named
    'sales_prediction' and 'confidence' respectively. The join_columns will be joined to join_features so that the
    target columns can be queried in tandem with the join_features and aggregate properly. If the join_columns already
    match the names of the categorical features in the data model, join_features can be omitted to use the names of the
    join_columns. The measures will be created from a QDS (Queried Dataset) which uses the following query:
    'SELECT <target_column1, target_column2, ... target_columnN, join_column1, join_column2, ...> FROM <udf_call>'
    By default, the created features will aggregate by sum, the aggregation method can be altered by
    calling data_model.update_aggregate_feature

    Args:
        data_model (DataModel): The AtScale data model to create the new features in
        target_columns (List[str]): A list of target columns which will be made into features, proper quoting for the
            data warehouse used is required. Feature names will be based on the name of the column as queried. These
            strings represent raw SQL and thus a target column can be a calculated column or udf call as long as it is
            proper SQL syntax.
        udf_call (str): A valid SQL statement that will be placed directly after a FROM clause and a space with no
        parenthesis.
        join_features (list, optional): a list of features in the data model to use for joining. If None it will not
            join the qds to anything. Defaults to None for no joins.
        join_columns (list, optional): The columns in the from statement to join to the join_features. List must be
            either None or the same length and order as join_features. Defaults to None to use identical names to the
            join_features. If multiple columns are needed for a single join they should be in a nested list.
            Data warehouse specific quoting is not required, join_columns should be passed as strings and if quotes are
            required for the data model's data warehouse, they will be inserted automatically.
        folder (str): Optionally specifies a folder to put the created features in. If the folder does not exist it will
            be created.
        qds_name (str): Optionally specifies the name of Queried Dataset that is created. Defaults to None to be named
            AI_LINK_UDF_QDS_<N> where <N> is 1 or the minimum number that doesn't conflict with existing dataset names.
        feature_inputs (List[str]): The names of features in data_model that are the inputs for the udf, in the order
            they are passed to the udf.
        warehouse_id (str): Defaults to None. The id of the warehouse that datasets in the data model query from.
            This parameter is only required if no dataset has been created in the data model yet.
        publish (bool): Defaults to True. Whether the updated project should be published or only the draft should be
            updated.

    Raises:
        atscale_errors.UserError: When new_feature_name already exists as a feature in the given data_model, or any
        feature in feature_inputs does not exist in the given data_model.
        """
    if join_features is None:
        join_features = []

    if join_columns is None:
        join_columns = join_features
    elif len(join_features) != len(join_columns):
        raise atscale_errors.UserError(f'join_features and join_columns must be equal lengths. join_features is'
                                       f' length {len(join_features)} while join_columns is length {len(join_columns)}')

    if qds_name is None:
        prefix = 'AI_LINK_UDF_QDS_'
        all_dsets = project_parser.get_datasets(project_dict=data_model.project._get_dict())
        count = 1
        number_taken = {}
        for dset in all_dsets:
            if dset["name"][:len(prefix)] == prefix:
                try:
                    number_taken[int(dset["name"][len(prefix):])] = True
                except:
                    pass
        while count in number_taken:
            count += 1
        qds_name = f'{prefix}{count}'
    warehouse_id = data_model.get_connected_warehouse() if warehouse_id is None else warehouse_id
    db_platform: enums.PlatformType = data_model.project.atconn._get_warehouse_platform(warehouse_id=warehouse_id)
    db_conn: SQLConnection = db_utils.enum_to_dbconn(platform_type=db_platform)
    q: str = db_conn._column_quote()  # ex. Snowflake.column_quote(), its a static method

    join_column_strings = [f'{q}{j}{q}' for j in join_columns]
    qds_query = f'SELECT {", ".join(target_columns + join_column_strings)} FROM {udf_call}'
    data_model.add_queried_dataset(warehouse_id=warehouse_id,
                                   dataset_name=qds_name,
                                   query=qds_query,
                                   join_features=join_features,
                                   join_columns=join_columns)
    columns = data_model.project.atconn.get_query_columns(warehouse_id=data_model.get_connected_warehouse(),
                                                          query=qds_query)
    target_column_names = []
    for i in range(len(target_columns)):
        target_column_names.append(columns[i][0])
    for new_feature in target_column_names:
        data_model.create_aggregate_feature(dataset_name=qds_name,
                                            column_name=new_feature,
                                            name=new_feature,
                                            aggregation_type=Aggs.SUM,
                                            caption=new_feature,
                                            folder=folder,
                                            publish=False)
    if publish:
        data_model.project.publish()

def _write_regression_model_checks(model_type:enums.ScikitLearnModelType,
                                   data_model:DataModel,
                                   regression_model,
                                   new_feature_name:str):
    """ A helper function for writing regression models to AtScale.

    Args:
        model_type (enums.ScikitLearnModelType): the type of scikit-learn model being written to AtScale.
        data_model (DataModel): The AtScale DataModel to add the regression into. 
        regression_model (LinearRegression): The scikit-learn LinearRegression model to build into a feature.
        new_feature_name (str): The name of the created feature.

    Raises:
        atscale_errors.UserError: When the model passed is not a valid scikit-learn model.
        atscale_errors.UserError: When a feature already exists with new_feature_name.
        atscale_errors.ImportError: When scikit-learn is not installed.
    """
    try:
        if model_type == enums.ScikitLearnModelType.LINEARREGRESSION:
            from sklearn.linear_model import LinearRegression
        elif model_type == enums.ScikitLearnModelType.LOGISTICREGRESSION:
            from sklearn.linear_model import LogisticRegression
    except ImportError:
        raise ImportError('scikit-learn needs to be installed to use this functionality, the function takes an '
                          f'sklearn.linear_model.{model_type} object. Try running pip install scikit-learn')

    model_failure = False

    if model_type == enums.ScikitLearnModelType.LINEARREGRESSION:
        if not isinstance(regression_model, LinearRegression):
            model_failure = True
    elif model_type == enums.ScikitLearnModelType.LOGISTICREGRESSION:
        if not isinstance(regression_model, LogisticRegression):
            model_failure = True

    if model_failure:
        raise atscale_errors.UserError(f'The model object of type: {type(regression_model)} is not compatible with this method '
                                       f'which takes an object of type sklearn.linear_model.{model_type}')
                                       
    if new_feature_name in data_model.get_features().keys():
        raise atscale_errors.UserError(f'Invalid name: \'{new_feature_name}\'. A feature already exists with that name')

def _write_regression_model(model_type:enums.ScikitLearnModelType,
                            data_model:DataModel,
                            regression_model,
                            new_feature_name:str,
                            feature_inputs:List[str],
                            granularity_levels:List[str]):
    """ A helper function for writing regression models to AtScale.

    Args:
        model_type (enums.ScikitLearnModelType): the type of scikit-learn model being written to AtScale.
        data_model (DataModel): The AtScale DataModel to add the regression into. 
        regression_model (sklearn.linear_model): The scikit-learn linear model to build into a feature.
        new_feature_name (str): The name of the created feature.
        feature_inputs (List[str], optional): List of names of inputs features in the input order.
            Defaults to None to use the column names used when training the model.
        granularity_levels (List[str], optional): List of lowest categorical levels that predictions with this
            model can be run on. Defaults to False to use the lowest level from each hierarchy.
    """
    if granularity_levels is None:
        hierarchy_to_levels: Dict['str', List[dict]] = dmv_utils.get_dmv_data(model=data_model,
                                                                              id_field=enums.Level.hierarchy,
                                                                              fields=[enums.Level.name,
                                                                                      enums.Level.level_number])
        leaf_levels: List[str] = []
        for levels in hierarchy_to_levels.values():
            if (type(levels['name']) == list):
                leaf_levels.append(levels['name'][-1])
            else:
                leaf_levels.append(levels['name'])
        granularity_levels = leaf_levels

    if feature_inputs is None:
        feature_inputs = list(regression_model.feature_names_in_)

    atscale_query: str = query_utils._generate_atscale_query(data_model=data_model,
                                                             feature_list=feature_inputs + granularity_levels)
    feature_query: str = query_utils.generate_db_query(data_model=data_model,
                                                       atscale_query=atscale_query,
                                                       use_aggs=False)
    categorical_string: str = ", ".join(f'"{cat}"' for cat in granularity_levels)
    numeric = ' + '.join([f'{theta1}*"{x}"' for theta1, x in zip(regression_model.coef_[0], regression_model.feature_names_in_)])
    numeric += f' + {regression_model.intercept_[0]}'
    if model_type == enums.ScikitLearnModelType.LINEARREGRESSION:
        qds_query: str = f'SELECT ({numeric}) as "{new_feature_name}" , {categorical_string} FROM ({feature_query})'
    elif model_type == enums.ScikitLearnModelType.LOGISTICREGRESSION:
        qds_query: str = f'SELECT ROUND(1 - 1 / (1 + POWER({e}, {numeric})), 0) as "{new_feature_name}" , {categorical_string} FROM ({feature_query})'
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

def write_linear_regression_model(data_model: DataModel,
                                  regression_model,
                                  new_feature_name: str,
                                  granularity_levels: List[str] = None,
                                  feature_inputs: List[str] = None):
    """ Writes a scikit-learn LinearRegression model, which takes AtScale features exclusively as input, to the given
    DataModel as a sum aggregated feature with the given name. The feature will return the output of the coefficients
    and intercept in the model applied to feature_inputs as defined in atscale. Omitting feature_inputs will use the
    names of the columns passed at training time and error if any names are not in the data model.

    Args:
        data_model (DataModel): The AtScale DataModel to add the regression into. 
        regression_model (LinearRegression): The scikit-learn LinearRegression model to build into a feature.
        new_feature_name (str): The name of the created feature.
        granularity_levels (List[str], optional): List of lowest categorical levels that predictions with this
            model can be run on. Defaults to False to use the lowest level from each hierarchy.
        feature_inputs (List[str], optional): List of names of inputs features in the input order.
            Defaults to None to use the column names used when training the model.
   
    Raises:
        atscale_errors.UserError: When the model passed is not a valid scikit-learn model.
        atscale_errors.UserError: When a feature already exists with new_feature_name.
        atscale_errors.ImportError: When scikit-learn is not installed.
    """
    model_utils._perspective_check(data_model)

    _write_regression_model_checks(enums.ScikitLearnModelType.LINEARREGRESSION,
                                   data_model,
                                   regression_model,
                                   new_feature_name)

    _write_regression_model(enums.ScikitLearnModelType.LINEARREGRESSION,
                            data_model,
                            regression_model,
                            new_feature_name,
                            feature_inputs,
                            granularity_levels)

def write_logistic_regression_model(data_model: DataModel,
                                    regression_model,
                                    new_feature_name: str,
                                    granularity_levels: List[str] = None,
                                    feature_inputs: List[str] = None):
    """ Writes a scikit-learn binary LogisticRegression model, which takes AtScale features exclusively as input, to the given
    DataModel as a sum aggregated feature with the given name. The feature will return the output of the coefficients
    and intercept in the model applied to feature_inputs as defined in atscale. Omitting feature_inputs will use the
    names of the columns passed at training time and error if any names are not in the data model.
    
    Args:
        data_model (DataModel): The AtScale DataModel to add the regression into. 
        regression_model (LogisticRegression): The scikit-learn LogisticRegression model to build into a feature.
        new_feature_name (str): The name of the created feature.
        granularity_levels (List[str], optional): List of lowest categorical levels that predictions with this
            model can be run on. Defaults to False to use the lowest level from each hierarchy.
        feature_inputs (List[str], optional): List of names of inputs features in the input order.
            Defaults to None to use the column names used when training the model.
    
    Raises:
        atscale_errors.UserError: When the model passed is not a valid scikit-learn model.
        atscale_errors.UserError: When a feature already exists with new_feature_name.
        atscale_errors.ImportError: When scikit-learn is not installed.
    """
    model_utils._perspective_check(data_model)

    _write_regression_model_checks(enums.ScikitLearnModelType.LOGISTICREGRESSION,
                                   data_model,
                                   regression_model,
                                   new_feature_name)

    # NOTE: Function only supports binary classification; AI-Link has not implemented multiclass support yet. We only support 
    # binary classification until customer feedback indicates multiclass would be of use, as it is non-trivial to expand the logic. 
    if len(regression_model.classes_) > 2:
        raise atscale_errors.UserError(f'write_logistic_regression_model only supports binary classification; model: '
                                       f'{regression_model} has more than two classes')

    _write_regression_model(enums.ScikitLearnModelType.LOGISTICREGRESSION,
                            data_model,
                            regression_model,
                            new_feature_name,
                            feature_inputs,
                            granularity_levels)
