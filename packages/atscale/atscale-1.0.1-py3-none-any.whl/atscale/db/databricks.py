import logging

import pandas
import pandas as pd
from atscale.db.database import Database


class Databricks(Database):
    """An object used for all interaction between AtScale and Databricks as well as storage of all necessary
            information for the connected Databricks database"""

    def __init__(self, atscale_connection_id, token, host, schema, http_path, port=443):
        """ Creates a database connection to allow for writeback to a Databricks warehouse.

        :param str atscale_connection_id: The connection name for the warehouse in AtScale.
        :param str token: The database token.
        :param str host: The host.
        :param str http_path: The database HTTP path.
        :param str port: The database port (defaults to 443).
        """
        try:
            from sqlalchemy import create_engine
        except ImportError as e:
            from atscale.errors import AtScaleExtrasDependencyImportError
            raise AtScaleExtrasDependencyImportError('databricks', str(e))

        for parameter in [atscale_connection_id, token, host, schema, http_path, port]:
            if not parameter:
                raise Exception('One or more of the given parameters are None or Null, all must be included to create'
                                'a connection')
        super().__init__(atscale_connection_id=atscale_connection_id,
                       database=None,
                       schema=schema)
        #todo: check which parameter is the database field in json of connection-groups/orgId/default

        engine = create_engine(f'databricks+connector://token:{token}@{host}:{port}/{schema}',
                               connect_args={'http_path': http_path})
        connection = engine.connect()
        connection.close()

        self.connection_string = str(engine.url)
        self.http_path = http_path
        logging.info('Databricks database created')

    def _add_table_internal(self, table_name: str, dataframe: pandas.DataFrame, chunksize: int=10000,
                           if_exists: str='fail'):
        """ Creates a table in Databricks using a pandas DataFrame.

                :param str table_name: The table to insert into.
                :param pandas.DataFrame dataframe: The DataFrame to upload to the table.
                :param int chunksize: the number of rows to insert at a time. Defaults to None to use default value for database.
                :param string if_exists: what to do if the table exists. Valid inputs are 'append', 'replace', and 'fail'. Defaults to 'fail'.
                """
        from sqlalchemy import create_engine

        engine = create_engine(self.connection_string, connect_args={'http_path': self.http_path})
        dataframe.to_sql(name=table_name, con=engine, schema=self.schema, method='multi', index=False,
                  chunksize=chunksize, if_exists=if_exists)

        logging.info(f'Table \"{table_name}\" created in Databricks with {dataframe.size} rows and {len(dataframe.columns)} columns')

    def submit_query(self, db_query):
        """ Submits a query to Snowflake and returns the result.

        :param str db_query: The query to submit to the database.
        :return: The queried data.
        :rtype: pandas.DataFrame
        """
        from sqlalchemy import create_engine
        engine = create_engine(self.connection_string, connect_args={'http_path': self.http_path})
        connection = engine.connect()
        df = pd.read_sql_query(db_query, connection)
        return df