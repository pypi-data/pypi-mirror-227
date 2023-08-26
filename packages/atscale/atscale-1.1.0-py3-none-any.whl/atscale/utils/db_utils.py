import logging
from typing import Tuple, Dict
from atscale.connection import Connection
from atscale.db.sql_connection import SQLConnection
from atscale import atscale_errors
from atscale.utils.enums import TableExistsActionType
from pandas import DataFrame


#D
def write_dataframe_to_db(atconn: Connection, dbconn: SQLConnection, table_name: str, warehouse_id: str, dataframe: DataFrame,
                          if_exists: TableExistsActionType = TableExistsActionType.FAIL) -> Tuple[str, Dict]:
    """Creates a table in the data warehouse and populates it with the data from the given DataFrame

    Args:
        atconn (Connection): The AtScale connection to use
        dbconn (SQLConnection): The sql connection to use to connect to interact with the data warehouse
        table_name (str): The name of the table to create
        warehouse_id (str): The id of the warehouse for AtScale to use to reach the new table
        dataframe (DataFrame): The dataframe containing the data to populate the table with
        if_exists (TableExistsActionType, optional): What to do if a table already exists with that name. Defaults to TableExistsActionType.FAIL.
    
    Returns:
        Tuple[str, Dict]: A tuple with the name of the table found within Atscale, and a dictionary of the converted column names
    """
    fixed_table_name = dbconn._fix_table_name(table_name)
    fixed_df = dataframe.rename(columns=lambda c: dbconn._fix_column_name(c))
    dbconn.write_df_to_db(dataframe=fixed_df, table_name=fixed_table_name, if_exists=if_exists)

    database = None
    schema = None
    if hasattr(dbconn, 'database'):
        database = dbconn.database
    if hasattr(dbconn, 'schema'):
        schema = dbconn.schema

    atscale_tables  = atconn.get_tables(warehouse_id, database, schema)
    if table_name in atscale_tables:
        atscale_table_name = table_name
    elif table_name.upper() in atscale_tables:
        atscale_table_name = table_name.upper()
        logging.warn(f'Table name: {table_name} appears as {atscale_table_name}')
    elif table_name.lower() in atscale_tables:
        atscale_table_name = table_name.lower()
        logging.warn(f'Table name: {table_name} appears as {atscale_table_name}')
    else:
        raise atscale_errors.UserError(f'Unable to find table: {table_name} after write. If the table exists make sure AtScale has access to it')
    
    atscale_columns = [c[0] for c in atconn.get_table_columns(warehouse_id=warehouse_id,
                                                              table_name=atscale_table_name,
                                                              database=database,
                                                              schema=schema)]
    column_dict = {}
    for col in dataframe.columns:
        if col in atscale_columns:
            column_dict[col] = col
        elif col.upper() in atscale_columns:
            atscale_col = col.upper()
            column_dict[col] = atscale_col
            logging.warn(f'Column name: {col} appears as {atscale_col}')
        elif col.lower() in atscale_columns:
            atscale_col = col.lower()
            column_dict[col] = atscale_col
            logging.warn(f'Table name: {table_name} appears as {atscale_col}')
        else:
            raise atscale_errors.UserError(f'Unable to find column: {col} in table: {table_name}.')

    return atscale_table_name, column_dict