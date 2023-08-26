import re
from math import sqrt
from atscale.db.sql_connection import SQLConnection
from atscale.data_model.data_model import DataModel
from typing import List, Dict
from atscale.base.enums import PlatformType
from atscale.errors.atscale_errors import UserError, EDAException
from atscale.utils.metadata_utils import (
    _get_all_numeric_feature_names,
    _get_all_categorical_feature_names,
)
from atscale.utils.model_utils import _check_features
from atscale.utils.query_utils import _generate_atscale_query, generate_db_query
from atscale.base.enums import PlatformType, PandasTableExistsActionType
import random
import string
import logging
import numpy as np


logger = logging.getLogger(__name__)


class Stats:
    def __init__(self):
        self.base_table_granularity_level = ""
        self.base_table_numeric_features = set()
        self.query_dict = {
            "var": {},  # Populated with features as keys if variance is requested, None values –
            # these values to be set with actual variance
            "cov": None,  # Value set to list of two features if covariance is requested
        }


def _stats_checks(
    dbconn: SQLConnection,
    data_model: DataModel,
    feature_list: List[str],
    granularity_level: List[str],
    if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL,
) -> None:
    """Runs checks on parameters passed to the below functions.
    Args:
        dbconn (SQLConnection): The database connection to interact with.
        data_model (DataModel): The data model corresponding to the features provided.
        feature_list (List[str]): The feature(s) involved in the calculation.
        granularity_level (List[str]): The categorical feature corresponding to the level of
                                       granularity desired in the given feature.

    Raises:
        UserError: Given dbconn must be to Snowflake or Databricks at this point.
        UserError: User can't select APPEND as an ActionType.

    Returns:
        None.
    """
    if (
        dbconn.platform_type != PlatformType.SNOWFLAKE
        and dbconn.platform_type != PlatformType.DATABRICKS
    ):
        raise UserError(
            f"This function is only supported for Snowflake and Databricks at this time."
        )

    if if_exists == PandasTableExistsActionType.APPEND:
        raise UserError(
            f"The ActionType of APPEND is not valid for this function, only REPLACE AND FAIL are valid."
        )

    all_numeric_features = _get_all_numeric_feature_names(data_model)
    all_categorical_features = _get_all_categorical_feature_names(data_model)

    # Check that features exist in the given DataModel in the first place
    _check_features(
        feature_list + granularity_level, all_numeric_features + all_categorical_features
    )

    # Check that numeric/categorical features are in correct categories
    _check_features(
        feature_list,
        all_numeric_features,
        errmsg="Make sure feature is a numeric feature",
    )

    _check_features(
        granularity_level,
        all_categorical_features,
        errmsg="Make sure granularity_level is a categorical feature",
    )


def _connection_wrapper(
    dbconn: SQLConnection,
    data_model: DataModel,
    stats_obj: Stats,
    sample: bool = True,
    if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL,
) -> None:
    """Wrapper to minimize db connections when below functions are called
    dbconn (SQLConnection): The database connection to interact with.
    data_model (DataModel): The data model corresponding to the features provided.
    stats_obj (Stats): Stores variance and covariance values for a given connection.
    sample (bool, optional): Whether to calculate the sample variance. Defaults to True; otherwise,
                             calculates the population variance.
    if_exists (PandasTableExistsActionType, optional): The default action that taken when creating
                                                       a table with a preexisting name. Does not accept APPEND. Defaults to FAIL.
    """
    uuid_str = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    base_table_name = f"atscale_stats_tbl_{uuid_str}"
    logger.info(f"generating temp stats tables: {base_table_name}")

    base_table_atscale_query = generate_db_query(
        data_model=data_model,
        atscale_query=_generate_atscale_query(
            data_model=data_model,
            feature_list=list(stats_obj.base_table_numeric_features)
            + [stats_obj.base_table_granularity_level],
        ),
    )

    # Initialize base table
    base_table_query = f"CREATE TABLE {base_table_name} AS ({base_table_atscale_query}); "

    try:
        dbconn.submit_query(base_table_query)
    except Exception as e:
        err_msg = str(e)
        if "already exists." in err_msg:
            if if_exists == PandasTableExistsActionType.REPLACE:
                try:
                    dbconn.submit_query(f"DROP TABLE IF EXISTS {base_table_name}; ")
                    dbconn.submit_query(base_table_query)
                except Exception as e:
                    raise e
            else:
                table_name = re.search("Object (.*?) already exists", err_msg).group(1)
                raise UserError(
                    f"A table already exists with name: {table_name}. Name collisions between runs are rare "
                    f"but can happen. You can avoid this error by setting if_exists to REPLACE"
                )
        else:
            raise e

    for query_key in stats_obj.query_dict:
        if query_key == "var":
            if stats_obj.query_dict[query_key] != {}:
                for var_key in stats_obj.query_dict[query_key]:
                    if sample:
                        var = (
                            f"SELECT (SELECT (1. / (COUNT({var_key}) - 1)) FROM {base_table_name}) * "
                            f"SUM(POWER((SELECT AVG({var_key}) FROM {base_table_name}) - {var_key}, 2)) "
                            f"FROM {base_table_name}; "
                        )
                    else:
                        var = (
                            f"SELECT (SELECT (1. / COUNT({var_key})) FROM {base_table_name}) * "
                            + f"SUM(POWER((SELECT AVG({var_key}) FROM {base_table_name}) - {var_key}, 2))"
                            + f"FROM {base_table_name}; "
                        )
                    stats_obj.query_dict[query_key][var_key] = dbconn.submit_query(var)

        elif query_key == "cov":
            if stats_obj.query_dict[query_key] is not None:
                fl = stats_obj.query_dict[query_key]
                f1 = fl[0]
                f2 = fl[1]
                if sample:
                    cov = (
                        f"SELECT (SELECT (1. / (COUNT(*) - 1)) FROM {base_table_name}) * SUM( "
                        + f"((SELECT AVG({f1}) FROM {base_table_name}) - {f1}) * "
                        + f"((SELECT AVG({f2}) FROM {base_table_name}) - {f2})) "
                        + f"FROM {base_table_name}; "
                    )

                else:
                    cov = (
                        f"SELECT (SELECT (1. / COUNT(*)) FROM {base_table_name}) * SUM( "
                        + f"((SELECT AVG({f1}) FROM {base_table_name}) - {f1}) * "
                        + f"((SELECT AVG({f2}) FROM {base_table_name}) - {f2})) "
                        + f"FROM {base_table_name}; "
                    )

                stats_obj.query_dict["cov"] = dbconn.submit_query(cov)

        else:
            raise EDAException(
                f'query_key: "{query_key}" is invalid. Valid options are "var" and "cov".'
            )

    # Drop base table
    dbconn.submit_query(f"DROP TABLE {base_table_name};")


def var(
    dbconn: SQLConnection,
    data_model: DataModel,
    feature: str,
    granularity_level: str,
    sample: bool = True,
    if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL,
) -> float:
    """Returns the variance of a given feature.
    Args:
        dbconn (SQLConnection): The database connection to interact with.
        data_model (DataModel): The data model corresponding to the features provided.
        feature_list (str): The feature whose variance is calculated.
        granularity_level (str): The categorical feature corresponding to the level of
                                 granularity desired in the given feature.
        sample (bool, optional): Whether to calculate the sample variance. Defaults to True; otherwise,
                                 calculates the population variance.
        if_exists (PandasTableExistsActionType, optional): The default action that taken when creating
                                                           a table with a preexisting name. Does not accept APPEND. Defaults to FAIL.

    Returns:
        float: The feature's variance.
    """
    # Error checks
    _stats_checks(
        dbconn=dbconn,
        data_model=data_model,
        feature_list=[feature],
        granularity_level=[granularity_level],
    )

    stats_obj = Stats()

    stats_obj.base_table_granularity_level = granularity_level
    stats_obj.base_table_numeric_features = {feature}
    stats_obj.query_dict = {"var": {feature: 0.0}, "cov": None}

    _connection_wrapper(
        dbconn=dbconn,
        stats_obj=stats_obj,
        data_model=data_model,
        sample=sample,
        if_exists=if_exists,
    )

    var = np.array(stats_obj.query_dict["var"][feature])[0][0]

    return var


def std(
    dbconn: SQLConnection,
    data_model: DataModel,
    feature: str,
    granularity_level: str,
    sample: bool = True,
    if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL,
) -> float:
    """Returns the standard deviation of a given feature.
    Args:
        dbconn (SQLConnection): The database connection to interact with.
        data_model (DataModel): The data model corresponding to the features provided.
        feature (str): The feature whose standard deviation is calculated.
        granularity_level (str): The categorical feature corresponding to the level of
                                 granularity desired in the given feature.
        sample (bool, optional): Whether to calculate the sample standard deviation. Defaults to True;
                                 otherwise, calculates the population standard deviation.
        if_exists (PandasTableExistsActionType, optional): The default action that taken when creating
                                                           a table with a preexisting name. Does not accept APPEND. Defaults to FAIL.

    Returns:
        float: The feature's standard deviation.
    """
    return sqrt(
        var(
            dbconn=dbconn,
            data_model=data_model,
            feature=feature,
            granularity_level=granularity_level,
            sample=sample,
            if_exists=if_exists,
        )
    )


def cov(
    dbconn: SQLConnection,
    data_model: DataModel,
    feature1: str,
    feature2: str,
    granularity_level: str,
    sample: bool = True,
    if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL,
) -> float:
    """Returns the covariance of two given features.
    Args:
        dbconn (SQLConnection): The database connection to interact with.
        data_model (DataModel): The data model corresponding to the features provided.
        feature1 (str): The first feature.
        fearure2 (str): The second feature.
        granularity_level (str): The categorical feature corresponding to the level of
                                 granularity desired in the given features.
        sample (bool, optional): Whether to calculate the sample covariance. Defaults to True; otherwise,
                                 calculates the population covariance.
        if_exists (PandasTableExistsActionType, optional): The default action that taken when creating
                                                           a table with a preexisting name. Does not accept APPEND. Defaults to FAIL.

    Returns:
        float: The features' covariance.
    """
    # Error checks
    _stats_checks(
        dbconn=dbconn,
        data_model=data_model,
        feature_list=[feature1, feature2],
        granularity_level=[granularity_level],
    )

    stats_obj = Stats()

    stats_obj.base_table_granularity_level = granularity_level
    stats_obj.base_table_numeric_features = {feature1, feature2}
    stats_obj.query_dict = {"var": {}, "cov": [feature1, feature2]}

    _connection_wrapper(
        dbconn=dbconn,
        data_model=data_model,
        stats_obj=stats_obj,
        sample=sample,
        if_exists=if_exists,
    )

    cov = np.array(stats_obj.query_dict["cov"])[0][0]

    return cov


def corrcoef(
    dbconn: SQLConnection,
    data_model: DataModel,
    feature1: str,
    feature2: str,
    granularity_level: str,
    if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL,
) -> float:
    """Returns the correlation of two given features.
    Args:
        dbconn (SQLConnection): The database connection to interact with.
        data_model (DataModel): The data model corresponding to the features provided.
        feature1 (str): The first feature.
        fearure2 (str): The second feature.
        granularity_level (str): The categorical feature corresponding to the level of
                                 granularity desired in the given features.
        if_exists (PandasTableExistsActionType, optional): The default action that taken when creating
                                                           a table with a preexisting name. Does not accept APPEND. Defaults to FAIL.

    Returns:
        float: The features' correlation.
    """
    # Error checks
    _stats_checks(
        dbconn=dbconn,
        data_model=data_model,
        feature_list=[feature1, feature2],
        granularity_level=[granularity_level],
    )

    stats_obj = Stats()

    stats_obj.base_table_granularity_level = granularity_level
    stats_obj.base_table_numeric_features = {feature1, feature2}
    stats_obj.query_dict = {"var": {feature1: 0.0, feature2: 0.0}, "cov": [feature1, feature2]}

    _connection_wrapper(
        dbconn=dbconn,
        data_model=data_model,
        stats_obj=stats_obj,
        if_exists=if_exists,
    )

    v1 = np.array(stats_obj.query_dict["var"][feature1])[0][0]
    v2 = np.array(stats_obj.query_dict["var"][feature2])[0][0]
    cov = np.array(stats_obj.query_dict["cov"])[0][0]

    return cov / sqrt(v1 * v2)
