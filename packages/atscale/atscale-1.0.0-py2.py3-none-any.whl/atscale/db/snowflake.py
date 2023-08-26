import getpass
import logging
import os
import string
import random
from tempfile import TemporaryDirectory
from typing import Iterator, Tuple, cast, Dict, List

import pandas as pd

from atscale.db.database import Database
from atscale.errors import UserError


class Snowflake(Database):
    """
    An object used for all interaction between AtScale and Snowflake as well as storage of all necessary information
    for the connected Snowflake
    """
    def __init__(self, atscale_connection_id: str, username: str, account: str, warehouse: str,
                 database: str, schema: str, password: str = None):
        """ Creates a database connection to allow for writeback to a Snowflake warehouse.

        :param str username: The database username.
        :param str account: The database account.
        :param str warehouse: The database warehouse.
        :param str database: The database name.
        :param str schema: The database schema.
        """
        try:
            from snowflake.connector import connect
        except ImportError as e:
            from atscale.errors import AtScaleExtrasDependencyImportError
            raise AtScaleExtrasDependencyImportError('snowflake', str(e))

        for parameter in [atscale_connection_id, username, account, warehouse, database, schema]:
            if not parameter:
                raise Exception('One or more of the given parameters are None or Null, all must be included to create'
                                'a connection')
        if password is None:
            password = getpass.getpass(prompt='Password: ')

        conx = connect(account=account,
                       user=username,
                       password=password,
                       database=database,
                       schema=schema,
                       warehouse=warehouse,)
        conx.close()

        super().__init__(atscale_connection_id=atscale_connection_id,
                       database=database,
                       schema=schema)

        #saved for feast config (yaml) file and snowflake connector in queries
        self.username = username
        self.password = password
        self.warehouse = warehouse
        self.account = account

        logging.info('Snowflake db connection created')

    def _add_table_internal(self, table_name, dataframe: pd.DataFrame, chunksize=10000, if_exists='fail'):
        """ Inserts a DataFrame into table.

        :param str table_name: The table to insert into.
        :param pandas.DataFrame dataframe: The DataFrame to upload to the table.
        :param int chunksize: the number of rows to insert at a time. Defaults to None to use default value for database.
        :param string if_exists: what to do if the table exists. Valid inputs are 'append', 'replace', and 'fail'. Defaults to 'fail'.
        """
        from snowflake.connector import connect

        df = dataframe.copy()

        # Snowflake Specific, everything above could be abstracted into atscale.py or possibly Database class

        new_cols = []
        for col in df.columns:
            new_cols.append(self.fix_table_name(str(col)))
        df.columns = new_cols
        table_name = self.fix_table_name(table_name)

        conx = connect(account=self.account,
                       user=self.username,
                       password=self.password,
                       database=self.database,
                       schema=self.schema,
                       warehouse=self.warehouse)
        cur = conx.cursor()
        if if_exists == 'replace':
            create_tbl_statement = f'create or replace table "{self.database}"."{self.schema}"."{table_name}"'
        else:
            create_tbl_statement = f'create table "{self.database}"."{self.schema}"."{table_name}"'

        cur.execute(f"""SELECT EXISTS (
           SELECT * FROM INFORMATION_SCHEMA.TABLES 
           WHERE  table_schema = '{self.schema}'
           AND    table_name   = '{table_name}'
           );""")
        exists = cur.fetchone()[0]
        if not exists or if_exists == "replace":
            create_tbl_statement += " (\n"
            for column in df.columns:
                if (
                        df[column].dtype.name == "int"
                        or df[column].dtype.name == "int64"
                ):
                    create_tbl_statement = create_tbl_statement + column + " int"
                elif df[column].dtype.name == "object":
                    create_tbl_statement = create_tbl_statement + column + " varchar(16777216)"
                elif df[column].dtype.name == "datetime64[ns]":
                    create_tbl_statement = create_tbl_statement + column + " datetime"
                elif df[column].dtype.name == "float64":
                    create_tbl_statement = create_tbl_statement + column + " float8"
                elif df[column].dtype.name == "bool":
                    create_tbl_statement = create_tbl_statement + column + " boolean"
                else:
                    create_tbl_statement = create_tbl_statement + column + " varchar(16777216)"

                # If column is not last column, add comma, else end sql-query
                if df[column].name != df.columns[-1]:
                    create_tbl_statement = create_tbl_statement + ",\n"
                else:
                    create_tbl_statement = create_tbl_statement + ")"
            cur.execute(create_tbl_statement)
        if if_exists == 'fail':
            if exists:
                raise Exception(f"The table {table_name} already exists in {self.database}.{self.schema}")

        write_pandas(conx, df, table_name)
        conx.close()
        logging.info(f'Table \"{table_name}\" created in Snowflake '
                     f'with {df.size} rows and {len(df.columns)} columns \n using chunksize {chunksize}')

    def submit_query(self, db_query) -> pd.DataFrame:
        """ Submits a query to Snowflake and returns the result.

        :param: str db_query The query to submit to the database.
        :return: The queried data.
        :rtype: pandas.DataFrame
        """
        from snowflake.connector import connect
        conx = connect(account=self.account,
                       user=self.username,
                       password=self.password,
                       database=self.database,
                       schema=self.schema,
                       warehouse=self.warehouse,)
        cur = conx.cursor()
        cur.execute(db_query)
        all_rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        cur.close()
        conx.close()
        df = pd.DataFrame(all_rows)
        try:
            df.columns = field_names
        except Exception as e:
            raise Exception("The query returned no rows")
        return df

    def validate(self, data: dict):
        if data['platformType'] != 'snowflake':
            raise UserError(f'You are attempting to instantiate a snowflake database object with a atscale connection '
                            f'configured for {data["platformType"]}')
        if data['database'] != self.database: #watch out for upper/lower case
            raise UserError(f'The database referenced by atscale_connection_id {self.atscale_connection_id} does not '
                            f'match the field set: {self.database}')

    def fix_table_name(self, table_name: str) -> str:
        """Returns table_name.upper() and replaces - with _"""
        temp = '_'.join(table_name.split('-')).upper()
        temp = '_'.join(temp.split())
        return temp

def write_pandas(
    conn,
    df: pd.DataFrame,
    table_name: str,
    database: str = None,
    schema: str = None,
    chunk_size: int = None,
    compression: str = "gzip",
    on_error: str = "abort_statement",
    parallel: int = 4,
    quote_identifiers: bool = True,
    auto_create_table: bool = False,
    create_temp_table: bool = False,):
    """Allows users to most efficiently write back a pandas DataFrame to Snowflake.

    It works by dumping the DataFrame into Parquet files, uploading them and finally copying their data into the table.

    Returns whether all files were ingested correctly, number of chunks uploaded, and number of rows ingested
    with all of the COPY INTO command's output for debugging purposes.

        Example usage:
            import pandas
            from snowflake.connector.pandas_tools import write_pandas

            df = pandas.DataFrame([('Mark', 10), ('Luke', 20)], columns=['name', 'balance'])
            success, nchunks, nrows, _ = write_pandas(cnx, df, 'customers')

    Args:
        conn: Connection to be used to communicate with Snowflake.
        df: Dataframe we'd like to write back.
        table_name: Table name where we want to insert into.
        database: Database schema and table is in, if not provided the default one will be used (Default value = None).
        schema: Schema table is in, if not provided the default one will be used (Default value = None).
        chunk_size: Number of elements to be inserted once, if not provided all elements will be dumped once
            (Default value = None).
        compression: The compression used on the Parquet files, can only be gzip, or snappy. Gzip gives supposedly a
            better compression, while snappy is faster. Use whichever is more appropriate (Default value = 'gzip').
        on_error: Action to take when COPY INTO statements fail, default follows documentation at:
            https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html#copy-options-copyoptions
            (Default value = 'abort_statement').
        parallel: Number of threads to be used when uploading chunks, default follows documentation at:
            https://docs.snowflake.com/en/sql-reference/sql/put.html#optional-parameters (Default value = 4).
        quote_identifiers: By default, identifiers, specifically database, schema, table and column names
            (from df.columns) will be quoted. If set to False, identifiers are passed on to Snowflake without quoting.
            I.e. identifiers will be coerced to uppercase by Snowflake.  (Default value = True)
        auto_create_table: When true, will automatically create a table with corresponding columns for each column in
            the passed in DataFrame. The table will not be created if it already exists
        create_temp_table: Will make the auto-created table as a temporary table
    """
    from snowflake.connector.connection import SnowflakeCursor, SnowflakeConnection

    assert(isinstance(conn, SnowflakeConnection))
    if database is not None and schema is None:
        raise Exception(
            "Schema has to be provided to write_pandas when a database is provided"
        )
    # This dictionary maps the compression algorithm to Snowflake put copy into command type
    # https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html#type-parquet
    compression_map = {"gzip": "auto", "snappy": "snappy"}
    if compression not in compression_map.keys():
        raise Exception(
            "Invalid compression '{}', only acceptable values are: {}".format(
                compression, compression_map.keys()
            )
        )
    if quote_identifiers:
        location = (
            (('"' + database + '".') if database else "")
            + (('"' + schema + '".') if schema else "")
            + ('"' + table_name + '"')
        )
    else:
        location = (
            (database + "." if database else "")
            + (schema + "." if schema else "")
            + (table_name)
        )
    if chunk_size is None:
        chunk_size = len(df)
    cursor: SnowflakeCursor = conn.cursor()
    stage_name = create_temporary_sfc_stage(cursor)

    with TemporaryDirectory() as tmp_folder:
        for i, chunk in chunk_helper(df, chunk_size):
            chunk_path = os.path.join(tmp_folder, "file{}.txt".format(i))
            # Dump chunk into parquet file
            chunk.to_parquet(
                chunk_path,
                compression=compression,
                use_deprecated_int96_timestamps=True,
            )
            # Upload parquet file
            upload_sql = (
                "PUT /* Python:snowflake.connector.pandas_tools.write_pandas() */ "
                "'file://{path}' @\"{stage_name}\" PARALLEL={parallel}"
            ).format(
                path=chunk_path.replace("\\", "\\\\").replace("'", "\\'"),
                stage_name=stage_name,
                parallel=parallel,
            )
            logging.debug(f"uploading files with '{upload_sql}'")
            cursor.execute(upload_sql, _is_internal=True)
            # Remove chunk file
            os.remove(chunk_path)
    if quote_identifiers:
        columns = '"' + '","'.join(list(df.columns)) + '"'
    else:
        columns = ",".join(list(df.columns))

    if auto_create_table:
        file_format_name = create_file_format(compression, compression_map, cursor)
        infer_schema_sql = f"SELECT COLUMN_NAME, TYPE FROM table(infer_schema(location=>'@\"{stage_name}\"', file_format=>'{file_format_name}'))"
        logging.debug(f"inferring schema with '{infer_schema_sql}'")
        result_cursor = cursor.execute(infer_schema_sql, _is_internal=True)
        if result_cursor is None:
            raise Exception(infer_schema_sql)
        result = cast(List[Tuple[str, str]], result_cursor.fetchall())
        column_type_mapping: Dict[str, str] = dict(result)
        # Infer schema can return the columns out of order depending on the chunking we do when uploading
        # so we have to iterate through the dataframe columns to make sure we create the table with its
        # columns in order
        quote = '"' if quote_identifiers else ""
        create_table_columns = ", ".join(
            [f"{quote}{c}{quote} {column_type_mapping[c]}" for c in df.columns]
        )
        create_table_sql = (
            f"CREATE {'TEMP ' if create_temp_table else ''}TABLE IF NOT EXISTS {location} "
            f"({create_table_columns})"
            f" /* Python:snowflake.connector.pandas_tools.write_pandas() */ "
        )
        logging.debug(f"auto creating table with '{create_table_sql}'")
        cursor.execute(create_table_sql, _is_internal=True)
        drop_file_format_sql = f"DROP FILE FORMAT IF EXISTS {file_format_name}"
        logging.debug(f"dropping file format with '{drop_file_format_sql}'")
        cursor.execute(drop_file_format_sql, _is_internal=True)

    # in Snowflake, all parquet data is stored in a single column, $1, so we must select columns explicitly
    # see (https://docs.snowflake.com/en/user-guide/script-data-load-transform-parquet.html)
    if quote_identifiers:
        parquet_columns = "$1:" + ",$1:".join(f'"{c}"' for c in df.columns)
    else:
        parquet_columns = "$1:" + ",$1:".join(df.columns)
    copy_into_sql = (
        "COPY INTO {location} /* Python:snowflake.connector.pandas_tools.write_pandas() */ "
        "({columns}) "
        'FROM (SELECT {parquet_columns} FROM @"{stage_name}") '
        "FILE_FORMAT=(TYPE=PARQUET COMPRESSION={compression}) "
        "PURGE=TRUE ON_ERROR={on_error}"
    ).format(
        location=location,
        columns=columns,
        parquet_columns=parquet_columns,
        stage_name=stage_name,
        compression=compression_map[compression],
        on_error=on_error,
    )
    logging.debug("copying into with '{}'".format(copy_into_sql))
    # Snowflake returns the original cursor if the query execution succeeded.
    result_cursor = cursor.execute(copy_into_sql, _is_internal=True)
    if result_cursor is None:
        raise Exception(copy_into_sql)
    result_cursor.close()

def create_file_format(
    compression: str, compression_map: Dict[str, str], cursor
) -> str:
    file_format_name = (
        '"' + "".join(random.choice(string.ascii_lowercase) for _ in range(5)) + '"'
    )
    file_format_sql = (
        f"CREATE FILE FORMAT {file_format_name} "
        f"/* Python:snowflake.connector.pandas_tools.write_pandas() */ "
        f"TYPE=PARQUET COMPRESSION={compression_map[compression]}"
    )
    logging.debug(f"creating file format with '{file_format_sql}'")
    cursor.execute(file_format_sql, _is_internal=True)
    return file_format_name

def create_temporary_sfc_stage(cursor) -> str:
    stage_name = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
    create_stage_sql = (
        "create temporary stage /* Python:snowflake.connector.pandas_tools.write_pandas() */ "
        '"{stage_name}"'
    ).format(stage_name=stage_name)
    logging.debug(f"creating stage with '{create_stage_sql}'")
    result_cursor = cursor.execute(create_stage_sql, _is_internal=True)
    if result_cursor is None:
        raise Exception(create_stage_sql)
    result_cursor.fetchall()
    return stage_name

def chunk_helper(lst: pd.DataFrame, n: int) -> Iterator[Tuple[int, pd.DataFrame]]:
    """Helper generator to chunk a sequence efficiently with current index like if enumerate was called on sequence."""
    for i in range(0, len(lst), n):
        yield int(i / n), lst[i : i + n]
