import logging
from typing import List, Tuple, Dict
from atscale.connection.connection import Connection
from atscale.db.sql_connection import SQLConnection
from atscale.errors import atscale_errors
from atscale.base.enums import PandasTableExistsActionType
from pandas import DataFrame


def get_atscale_tablename(atconn: Connection, warehouse_id, database, schema, table_name: str):
    """Determines the tablename as referenced by AtScale. 

    Args:
        atconn (_type_): _description_
        warehouse_id (_type_): _description_
        database (_type_): _description_
        schema (_type_): _description_
        table_name (str): _description_

    Raises:
        atscale_errors.UserError: _description_

    Returns:
        _type_: _description_
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
            f'Unable to find table: {table_name} after write. If the table exists make sure AtScale has access to it')
    return atscale_table_name


def get_database_and_schema(dbconn: SQLConnection) -> Tuple[str, str]:
    database = None
    schema = None
    if hasattr(dbconn, 'database'):
        database = dbconn.database
    if hasattr(dbconn, 'schema'):
        schema = dbconn.schema
    return database, schema


def get_column_dict(atconn: Connection, dbconn: SQLConnection, warehouse_id: str, atscale_table_name: str,  dataframe_columns: List[str]) -> Dict:
    """Grabs columns from the AtScale table corresponding to the dataframe and compares columns from each, returning a dict where the
    keys are column names from the dataframe and the keys are the column names as they appear in the atscale_table_name. 

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


def conform_df_datatypes(df1: DataFrame, df2: DataFrame):
    """Converts all column dtypes of df2 to those of df1 to support calls of df1.equals(df2). df2 will be mutated in place. 
    One situation this was necessary for was pandas read_sql_query implementations which varied in the dtypes of the column of the
    dataframes it produced. For instance, the Snowflake vs BigQuery implementations both use pandas, but GBQ uses read_gbq which 
    produces dataframes with numeric columns with the dtype Int64 whereas Swnoflake defaults to read_sql_query which produces dataframes
    with numeric columns with the dtype int64. When trying to compare the result of submit_query() to a fixture dataframe its easiest to 
    use this to ensure the dtypes of the columns conform before a call to df1.equals(df2)

    Args:
        df1 (DataFrame): the dataframe with target dtypes for each column 
        df2 (DataFrame): the dataframe you want to conform to the dtypes for each column of df1. df2 must have the same column names as df1.
    """
    columns = list(df1)
    for col in columns:
        df1[col] = df1[col].astype(df2[col].dtype)
