from abc import ABC, abstractmethod

import pandas

from atscale.errors import UserError


class Database(ABC):
    """
    Database is an object used for interaction between AtScale python Api and the supported database

    Args:
        atscale_connection_id: the name of the connection to the data warehouse as set in the atscale design center.
        database: the name of the database or the instances synonymous level of organization
        schema: the name of the schema or the instance's synonymous level of organization
    """

    atscale_connection_id: str
    database: str
    schema: str

    def __init__(
        self,
        atscale_connection_id: str,
        database: str,
        schema: str
    ):
        self.atscale_connection_id = atscale_connection_id
        self.database = database
        self.schema = schema

    def add_table(self, table_name: str, dataframe: pandas.DataFrame, chunksize: int=None, if_exists: str='fail'):
        """ Creates a table in the database and inserts a DataFrame into the table. Checks chunksize and if_exists for
        bad inputs and then calls add_table_internal
        :param str table_name: What the table should be named.
        :param pandas.DataFrame dataframe: The DataFrame to upload to the table.
        :param int chunksize: the number of rows to insert at a time. Defaults to 10,000. If None, uses default
        :param string if_exists: what to do if the table exists. Valid inputs are 'append', 'replace',
        and 'fail'. Defaults to 'fail'.
        :raises UserError if chunksize is set to a value less than 1
        :raises Exception if 'if_exists' is not one of ['append', 'replace', 'fail']
        """
        if_exists = if_exists.lower()
        if if_exists not in ['append', 'replace', 'fail']:
            raise Exception(f'Invalid value for parameter \'if_exists\': {if_exists}. '
                            f'Valid values are \'append\', \'replace\', and \'fail\'')
        if chunksize is None:
            self._add_table_internal(table_name=table_name,
                                    dataframe=dataframe,
                                    if_exists=if_exists)
        else:
            if int(chunksize) < 1:
                raise Exception('Chunksize must be greater than 0 or not passed in to use default value')
            self._add_table_internal(table_name=table_name,
                                    dataframe=dataframe,
                                    chunksize=chunksize,
                                    if_exists=if_exists)

    @abstractmethod
    def _add_table_internal(self, table_name: str, dataframe: pandas.DataFrame, chunksize: int = None,
                           if_exists: str = 'fail'):
        """ Creates a table in the database and inserts a DataFrame into the table.
        :param str table_name: What the table should be named.
        :param pandas.DataFrame dataframe: The DataFrame to upload to the table.
        :param int chunksize: the number of rows to insert at a time. Defaults to 10,000. If None, uses default
        :param string if_exists: what to do if the table exists. Valid inputs are 'append', 'replace',
        and 'fail'. Defaults to 'fail'.
        """
        raise NotImplementedError

    @abstractmethod
    def submit_query(self, db_query):
        """ Submits a query to the database and returns the result.

        :param str db_query: The query to submit to the database.
        :return: The queried data.
        :rtype: pandas.DataFrame
        """
        raise NotImplementedError()

    def fix_table_name(self, table_name: str) -> str:
        """Returns an all caps or all lowercase version of the given name if the database requires,
        must use the same method on columns when adding a df to database"""
        return table_name

    def validate(self, data: dict):
        """Takes a dict of the connection group json from the atscale ui and throws an error if anything doesn't match
         up"""
        #if atscale recognizes a platformType as something other than the python class name lowercase, put translation
        type_dict = {
            "Snowflake": "somenameforsnowflake"
        }
        if self.__class__.__name__ in type_dict:
            platform = type_dict[self.__class__.__name__]
        else:
            platform = type_dict[self.__class__.__name__.lower()]

        if data["platformType"] != platform:
            raise UserError(f'You are trying to instantiate a {platform} database object based on connection_id '
                            f'referring to connection configured for {data["platformType"]}')
        if "database" in data:
            if data["database"] != self.database:
                raise UserError(f'The database referenced by atscale_connection_id {self.atscale_connection_id} does '
                                f'not match the field set: {self.database}')
