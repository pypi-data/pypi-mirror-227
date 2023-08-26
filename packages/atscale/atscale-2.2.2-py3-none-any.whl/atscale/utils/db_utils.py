import logging
from typing import List, Tuple, Dict
from atscale.connection.connection import Connection
from atscale.db.sql_connection import SQLConnection
from atscale.db.connections import bigquery, databricks, iris, mssql, redshift, snowflake, synapse
from atscale.errors import atscale_errors
from atscale.base import enums


def enum_to_dbconn(platform_type: enums.PlatformType) -> SQLConnection:
    """ takes enums.PlatformType enum and returns an uninstantiated object of the associated SQLConnection class"""
    mapping = {
        enums.PlatformType.GBQ: bigquery.BigQuery,
        enums.PlatformType.DATABRICKS: databricks.Databricks,
        enums.PlatformType.IRIS: iris.Iris,
        enums.PlatformType.MSSQL: mssql.MSSQL,
        enums.PlatformType.REDSHIFT: redshift.Redshift,
        enums.PlatformType.SNOWFLAKE: snowflake.Snowflake,
        enums.PlatformType.SYNAPSE: synapse.Synapse
        }
    return mapping[platform_type]


def get_atscale_tablename(atconn: Connection, warehouse_id: str, database: str, schema: str, table_name: str)->str:
    """Determines the tablename as referenced by AtScale. 

    Args:
        atconn (Connection):  The AtScale connection to use
        warehouse_id (str): The id in AtScale of the data warehouse to use
        database (str): The name of the database for the table
        schema (str): The name of the schema for the table
        table_name (str): The name of the table

    Raises:
        atscale_errors.UserError: If Atscale is unable to find the table this error will be raised

    Returns:
        str: The name AtScale shows for the table
    """
    atscale_tables = atconn.get_connected_tables(
        warehouse_id, database, schema)
    if table_name in atscale_tables:
        atscale_table_name = table_name
    elif table_name.upper() in atscale_tables:
        atscale_table_name = table_name.upper()
        logging.warning(
            f'Table name: {table_name} appears as {atscale_table_name}')
    elif table_name.lower() in atscale_tables:
        atscale_table_name = table_name.lower()
        logging.warning(
            f'Table name: {table_name} appears as {atscale_table_name}')
    else:
        raise atscale_errors.UserError(
            f'Unable to find table: {table_name}. If the table exists make sure AtScale has access to it')
    return atscale_table_name

def get_database_and_schema(dbconn: SQLConnection) -> Tuple[str, str]:
    """ Returns a tuple of the (database property, schema property) of the sqlconn object if those properties exist.
        For sqlconn objects with a 'catalog' property, the catalog will be returned instead of the database. 

    Args:
        dbconn (SQLConnection): The connection object to get properies from

    Returns:
        Tuple[str, str]: the (database, schema) if they exist. If catalog property exists, 
            instead returns (catalog, schema)
    """
    database = None
    schema = None

    if hasattr(dbconn, 'database'):
        database = dbconn.database
    if hasattr(dbconn, 'catalog'):
        database = dbconn.catalog
    if hasattr(dbconn, 'schema'):
        schema = dbconn.schema
    return database, schema

def get_column_dict(atconn: Connection, dbconn: SQLConnection, warehouse_id: str, atscale_table_name: str,  dataframe_columns: List[str]) -> Dict:
    """Grabs columns from the AtScale table corresponding to the dataframe and compares columns from each, returning a dict where the
    keys are column names from the dataframe and the values are the column names as they appear in the atscale_table_name. 

    Args:
        atconn (Connection):  The AtScale connection to use
        dbconn (SQLConnection): The sql connection to use to connect to interact with the data warehouse. Primary used here to get any database and schema references for the connection.
        warehouse_id (str): The id of the warehouse for AtScale to use to reach the new table
        atscale_table_name (str): the name of the table in the data warehouse as recognized by atscale that corresponds to the dataframe 
        dataframe_columns (List[str]): the DataFrame columns that corresponds to the atscale_table_name

    Raises:
        atscale_errors.UserError: Potential error if the dataframe features columns that are not found within the table referenced by atscale_table_name
    Returns:
        Dict: a Dict object where keys are the column names within the dataframe and the values are the columns as they appear in atscale_table_name as seen by AtScale. 
    """

    database, schema = get_database_and_schema(dbconn=dbconn)
    atscale_columns = [c[0] for c in atconn.get_table_columns(warehouse_id=warehouse_id,
                                                              table_name=atscale_table_name,
                                                              database=database,
                                                              schema=schema)]
    column_dict = {}
    #iterate over the dataframe columns, looking for near matches to accomodate databases auto capitalizing names
    for col in dataframe_columns:
        if col in atscale_columns:
            column_dict[col] = col
        elif col.upper() in atscale_columns:
            atscale_col = col.upper()
            column_dict[col] = atscale_col
            logging.warn(f'Column name: {col} appears as {atscale_col}')
        elif col.lower() in atscale_columns:
            atscale_col = col.lower()
            column_dict[col] = atscale_col
            logging.warn(f'Column name: {col} appears as {atscale_col}')
        else:
            raise atscale_errors.UserError(
                f'Unable to find column: {col} in table: {atscale_table_name}.')

    return column_dict

def _get_key_cols(dbconn: SQLConnection, key_dict: dict):
    """ If the provided key_dict requires a multi-column key (or has a key different from then value), then 
        run a query to get the contents of the other join columns.

    Args:
        dbconn (SQLConnection): The connection object to query if necessary
        key_dict (dict): The dictionary describing the necessary key columns

    Returns:
        dataframe (pd.DataFrame): The additional columns information needed for the join
    """
    # check the keys for the feature. If there are more than one or only one and it doesn't match the value we will need to pull in the columns we don't have
    if len(key_dict['key_cols']) > 1 or key_dict['key_cols'][0] != key_dict['value_col']:
        # if it is a qds we need to select from the query
        if key_dict['query']:
            table = key_dict['query']
        # if not we want to build the fully qualified table name
        else:
            table = f'"{key_dict["table_name"]}"'
            if key_dict["schema"]:
                table = f'"{key_dict["schema"]}".{table}'
            if key_dict["database"]:
                table = f'"{key_dict["database"]}".{table}'
        needed_cols = key_dict['key_cols']
        # the value column may or may not be one of the keys so add it if it is missing
        if key_dict['value_col'] not in needed_cols:
            needed_cols.append(key_dict['value_col'])
        column_string = '", "'.join(needed_cols)
        query = f'SELECT DISTINCT "{column_string}" FROM {table}'
        df_key = dbconn.submit_query(query)
        df_key.columns = needed_cols
        return df_key
    return None