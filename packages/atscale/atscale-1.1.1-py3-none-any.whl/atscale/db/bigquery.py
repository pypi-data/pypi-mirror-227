import os

from pandas import DataFrame

from atscale import atscale_errors
from atscale.db.sql_connection import SQLConnection
from atscale.utils.enums import PlatformType, TableExistsActionType


class BigQuery(SQLConnection):
    """The child class of SQLConnection whose implementation is meant to handle 
        interactions with Google BigQuery. 
    """
    platform_type: PlatformType = PlatformType.GBQ

    def __init__(self, gbq_project_id: str, dataset: str, credentials_path: str = None):
        """Constructs an instance of the BigQuery SQLConnection. Takes arguments necessary to find the project 
            and dataset. If credentials_path is not provided, it will prompt the user to login.

        Args:
            gbq_project_id (str): the gbq project id to connect to 
            dataset (str): the name of the dataset within gbq
            credentials_path (str, optional): The path to a credentials file. If provided, 
                this method will set the environment variable GOOGLE_APPLICATION_CREDENTIALS to 
                this value which is used automatically by GBQ auth methods. 
                See: https://googleapis.dev/python/google-api-core/latest/auth.html
                Defaults to None.
        """
        try:
            import pandas_gbq
    #        from sqlalchemy import create_engine
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError(
                'pandas_gbq', str(e))

        if None in [gbq_project_id, dataset]:
            raise ValueError(
                'One or more of the required parameters are None.')

        if credentials_path is not None:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self._gbq_project_id = gbq_project_id
        self._dataset = dataset

    @property
    def gbq_project_id(self) -> str:
        return self._gbq_project_id

    @gbq_project_id.setter
    def gbq_project_id(self, value):
        self._gbq_project_id = value
    #    SQLConnection.dispose_engine(self)

    @property
    def dataset(self) -> str:
        return self._dataset

    @dataset.setter
    def dataset(self, value):
        self._dataset = value
    #    SQLConnection.dispose_engine(self)

    # @property
    # def engine(self):
    #     if self._engine is not None:
    #         return self._engine
    #     from sqlalchemy import create_engine
    #     url = self._get_connection_url()
    #     self._engine = create_engine(url)
    #     return self._engine

    # @engine.setter
    # def engine(self, value):
    #     raise Exception(
    #         "It is not possible to set the engine. Please dispose, set parameters, then reference engine insead.")

    def get_connection_url(self):
        raise NotImplementedError

    def submit_queries(self, query_list: list) -> list:
        # see: https://pandas-gbq.readthedocs.io/en/latest/reading.html#
        # not using an SQLAlchemy engine or connection for this, but rather using the built
        # in pandas_gbq support.
        import pandas_gbq
        results = []
        for query in query_list:
            results.append(pandas_gbq.read_gbq(query, project_id=self.gbq_project_id))
        return results

    def submit_query(self, query) -> DataFrame:
        return self.submit_queries([query])[0]

    def write_df_to_db(self, table_name: str, dataframe: DataFrame,
                       if_exists: TableExistsActionType = TableExistsActionType.FAIL):
        # The code combined sqlalchemy with builtin pandas options if we have pandas_gbq installed.
        # I just went with pandas_gbq approaches direclty on a dataframe and removed sqlalchemy for now.
        # We're only wrapping pandas_gbq methods and not adding anythning here - the only reason to have this
        # is so we can pass in this object to a writeback method, along with a model, to verify the db and tables line up
        # and so that we control the actual table writing and then joining with the model in one method (to ensure those things line up).
        import pandas_gbq
        pandas_gbq.to_gbq(dataframe, f'{self.dataset}.{table_name}',
                          project_id=self.gbq_project_id, if_exists=if_exists.value)
