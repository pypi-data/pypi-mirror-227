from pandas import DataFrame
from atscale.utils.eda_utils import _get_pca_sql
from atscale.db.sql_connection import SQLConnection
from atscale.data_model import DataModel
from atscale.atscale_errors import EDAException
from atscale.utils.model_utils import check_features
from atscale.utils.query_utils import generate_atscale_query, generate_db_query
from typing import List, Tuple
from atscale.utils.metadata_utils import list_all_numeric_features, list_all_categorical_features


def pca(dbconn:SQLConnection, data_model:DataModel, pc_num:int, numeric_features:List[str], categorical_features:List[str]) -> Tuple[DataFrame, DataFrame]:
    """Performs principal component analysis (PCA) on the numeric features specified

    Args:
        dbconn (SQLConnection): The database connection that pca will interact with
        data_model (DataModel): The data model corresponding to the features provided
        pc_num (int): The number of principal components to be returned from the analysis. Must be in 
                      the range of [1, # of numeric features to be analyzed] (inclusive)
        numeric_features (List[str]): The numeric features to be analyzed via pca
        categorical_features (List[str]): The categorical features corresponding to the level of 
                                          granularity desired in numeric_features

    Raises:
        EDAException: User must be analyzing at least two numeric features
        EDAException: Number of PCs desired must be some positive integer less than or equal to the number of numeric features
                      being analyzed

    Returns:
        Tuple[DataFrame, DataFrame]: A pair of DataFrames, the first containing the PCs and the second containing 
                                     their percent weights 
    """
    dim = len(numeric_features)

    all_numeric_features = list_all_numeric_features(data_model)
    all_categorical_features = list_all_categorical_features(data_model)

    # Error checking
    ### Check that features exist in the given DataModel in the first place
    check_features(numeric_features + categorical_features, all_numeric_features + all_categorical_features)

    ### Check that numeric/categorical features are in correct categories
    check_features(numeric_features, all_numeric_features, errmsg='Make sure numeric_features consists only of numeric features')
    check_features(categorical_features, all_categorical_features, errmsg='Make sure categorical_features consists only of categorical features')

    if dim < 2:
        raise EDAException('Number of numeric features to be analyzed must be greater than or equal to 2')

    if type(pc_num) != int or pc_num > dim or pc_num <= 0:
        raise EDAException('Number of PCs must be some positive integer less than or equal to the number of features')

    # Initialize base table
    dbconn.submit_query('DROP TABLE IF EXISTS atscale_pca_base_table; ')

    base_table_query = 'CREATE TABLE atscale_pca_base_table AS ' + \
                       f'({generate_db_query(data_model=data_model, atscale_query=generate_atscale_query(data_model=data_model, feature_list=numeric_features + categorical_features))}); '

    dbconn.submit_query(base_table_query)

    # Generate queries to run PCA, display results, and drop all generated tables
    query_statements, drop_statements, display_statements = _get_pca_sql('atscale_pca_base_table', numeric_features, pc_num, dbconn.platform_type)

    # Run PCA off of base table
    dbconn.execute_statements(query_statements)

    # Get results
    pc_dataframe = dbconn.submit_query(display_statements['PCs'])
    weight_dataframe = dbconn.submit_query(display_statements['Weights'])

    # Drop everything written to DB
    dbconn.execute_statements(drop_statements)

    # Delete base table
    dbconn.submit_query('DROP TABLE atscale_pca_base_table; ')

    # Return tuple of DFs containing 1.) PCs and 2.) their weights
    return (pc_dataframe, weight_dataframe)
