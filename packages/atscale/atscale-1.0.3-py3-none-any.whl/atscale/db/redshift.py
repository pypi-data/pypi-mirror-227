import getpass
import logging

import pandas
import pandas as pd

from atscale.db.database import Database

class Redshift(Database):
    """
    An object used for all interaction between AtScale and Redshift as well as storage of all necessary information
    for the connected Redshift
    """
    def __init__(self, atscale_connection_id, username, host, database, schema, port='5439', password=None):
        """ Creates a database connection to allow for writeback to a Redshift warehouse.

        :param str atscale_connection_id: The connection name for the warehouse in AtScale.
        :param str username: The database username.
        :param str host: The host.
        :param str database: The database name.
        :param str schema: The database schema.
        :param str port: The database port (defaults to 5439).
        :raises Exception if any of the inputs are of type None
        """
        try:
            from sqlalchemy import create_engine
        except ImportError as e:
            from atscale.errors import AtScaleExtrasDependencyImportError
            raise AtScaleExtrasDependencyImportError('redshift', str(e))

        for parameter in [atscale_connection_id, username, host, database, schema, port]:
            if not parameter:
                raise Exception('One or more of the given parameters are None or Null, all must be included to create'
                                'a connection')

        if password is None:
            password = getpass.getpass(prompt='Password: ')

        super().__init__(atscale_connection_id=atscale_connection_id,
                       database=database,
                       schema=schema)

        engine = create_engine(f'redshift+redshift_connector://{username}:{password}@{host}:{port}/{database}')
        # the following line fixes a bug, not sure if the cause is sqlalchemy, sqlalchemy-redshift, or redshift-connector 
        # probably should try to remove when sqlalchemy 2.0 is released
        engine.dialect.description_encoding = None
        connection = engine.connect()
        connection.close()

        self.connection_string = str(engine.url)

        logging.info('Redshift connection created')

    def _add_table_internal(self, table_name: str, dataframe: pandas.DataFrame, chunksize: int=1000,
                           if_exists: str='fail'):
        """ Creates a table in redshift using a pandas DataFrame.

        :param str table_name: The table to insert into.
        :param pandas.DataFrame dataframe: The DataFrame to upload to the table.
        :param int chunksize: the number of rows to insert at a time. Defaults to None to use default value for database
        :param string if_exists: what to do if the table exists. Valid inputs are 'append', 'replace', and 'fail'.
        Defaults to 'fail'.
        """
        from sqlalchemy import create_engine

        engine = create_engine(self.connection_string)
        # the following line fixes a bug, not sure if the cause is sqlalchemy, sqlalchemy-redshift, or redshift-connector 
        # probably should try to remove when sqlalchemy 2.0 is released
        engine.dialect.description_encoding = None
        dataframe.to_sql(name=table_name, con=engine, schema=self.schema, method='multi', index=False,
                  chunksize=chunksize, if_exists=if_exists)
        logging.info(f'Table \"{table_name}\" created in Redshift with {dataframe.size} rows and {len(dataframe.columns)} columns')

    def submit_query(self, db_query):
        """ Submits a query to Redshift and returns the result.

        :param str db_query: The query to submit to the database.
        :return: The queried data.
        :rtype: pandas.DataFrame
        """
        from sqlalchemy import create_engine
        engine = create_engine(self.connection_string)
        # the following line fixes a bug, not sure if the cause is sqlalchemy, sqlalchemy-redshift, or redshift-connector 
        # probably should try to remove when sqlalchemy 2.0 is released
        engine.dialect.description_encoding = None
        connection = engine.connect()
        df = pd.read_sql_query(db_query, connection)
        return df