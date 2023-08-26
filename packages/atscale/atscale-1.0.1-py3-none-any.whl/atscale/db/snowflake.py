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
                 database: str, schema: str, password: str = None, role: str = None):
        """ Creates a database connection to allow for writeback to a Snowflake warehouse.

        :param str username: The database username.
        :param str account: The database account.
        :param str warehouse: The database warehouse.
        :param str database: The database name.
        :param str schema: The database schema.
        :param str role: The role to use (defaults to None to use the default role).
        :param str password: The password for the account (defaults to None to be prompted to enter).
        """
        try:
            from sqlalchemy import create_engine
            from snowflake.connector.pandas_tools import pd_writer
        except ImportError as e:
            from atscale.errors import AtScaleExtrasDependencyImportError
            raise AtScaleExtrasDependencyImportError('snowflake', str(e))

        for parameter in [atscale_connection_id, username, account, warehouse, database, schema]:
            if not parameter:
                raise Exception('One or more of the given parameters are None or Null, all must be included to create'
                                'a connection')
        if password is None:
            password = getpass.getpass(prompt='Password: ')

        super().__init__(atscale_connection_id=atscale_connection_id,
                       database=database,
                       schema=schema)
        if role:
            engine = create_engine(f'snowflake://{username}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}')
        else:
            engine = create_engine(f'snowflake://{username}:{password}@{account}/{database}/{schema}?warehouse={warehouse}')
        connection = engine.connect()
        connection.close()

        self.connection_string = str(engine.url)

        logging.info('Snowflake db connection created')

    def _add_table_internal(self, table_name, dataframe: pd.DataFrame, chunksize=10000, if_exists='fail'):
        """ Inserts a DataFrame into table.

        :param str table_name: The table to insert into.
        :param pandas.DataFrame dataframe: The DataFrame to upload to the table.
        :param int chunksize: the number of rows to insert at a time. Defaults to None to use default value for database.
        :param string if_exists: what to do if the table exists. Valid inputs are 'append', 'replace', and 'fail'. Defaults to 'fail'.
        """
        from sqlalchemy import create_engine
        from snowflake.connector.pandas_tools import pd_writer

        engine = create_engine(self.connection_string)
        fixed_table_name = self.fix_table_name(table_name)
        df = dataframe.rename(columns=lambda c: self.fix_column_name(c))
        df.to_sql(name=fixed_table_name, con=engine, schema=self.schema, if_exists=if_exists, index=False, chunksize=chunksize, method=pd_writer)
        logging.info(f'Table \"{fixed_table_name}\" created in Snowflake '
                     f'with {df.size} rows and {len(df.columns)} columns')

    def submit_query(self, db_query) -> pd.DataFrame:
        """ Submits a query to Snowflake and returns the result.

        :param: str db_query The query to submit to the database.
        :return: The queried data.
        :rtype: pandas.DataFrame
        """
        from sqlalchemy import create_engine
        engine = create_engine(self.connection_string)
        connection = engine.connect()
        df = pd.read_sql_query(db_query, connection)
        return df

    def fix_table_name(self, table_name: str) -> str:
        """Returns table_name in all uppercase characters"""
        return table_name.lower()

    def fix_column_name(self, column_name: str) -> str:
        """Returns column_name in all uppercase characters"""
        return column_name.upper()