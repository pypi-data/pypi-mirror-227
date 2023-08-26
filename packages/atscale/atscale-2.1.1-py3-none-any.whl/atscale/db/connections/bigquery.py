import inspect
import os
from pandas import DataFrame

from atscale.errors import atscale_errors
from atscale.db.sql_connection import SQLConnection
from atscale.base.enums import PlatformType, PandasTableExistsActionType


class BigQuery(SQLConnection):
    """The implements SQLConnection to handle interactions with Google BigQuery. 
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
        super().__init__()

        try:
            import pandas_gbq
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError(
                'gbq', str(e))

        localVars = locals()
        inspection = inspect.getfullargspec(self.__init__)
        # list of all parameters names in order (optionals must come after required)
        all_params = inspection[0]
        # tuple of default values (for every optional parameter)
        defaults = inspection[3]
        # parameter has default if and only if its optional
        param_name_list = all_params[:-len(defaults)]
        param_names_none = [x for x in param_name_list if localVars[x] is None]

        if param_names_none:
            raise ValueError(
                f'The following required parameters are None: {", ".join(param_names_none)}')

        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self._gbq_project_id = gbq_project_id
        self._dataset = dataset

    @property
    def gbq_project_id(self) -> str:
        return self._gbq_project_id

    @gbq_project_id.setter
    def gbq_project_id(self, value):
        self._gbq_project_id = value

    @property
    def dataset(self) -> str:
        return self._dataset

    @dataset.setter
    def dataset(self, value):
        self._dataset = value

    @property
    def schema(self) -> str:
        """Spoofing a schema property that returns the GBQ dataset

        Returns:
            str: the dataset returned as a schema property
        """
        return self._dataset

    # Perhaps bad form, but leaving this code snippet here for future potential purposes. This class used to implement
    # SQLAlchemyConnection. By uncommenting this it can again. This worked fine, however, the dialect version as of me
    # writing this generated a bunch of warnings from the main library. We were already using pandas_gbq for most things
    # anyway so I just wrote up an execute_statements that used the gbq client directly and removed the SQLAlchemy stuff.
    # def _get_connection_url(self):
    #     if self._credentials_path is not None:
    #         connection_url = f'bigquery://{self._gbq_project_id}/{self._dataset}?credentials_path={self._credentials_path}'
    #     else:
    #         connection_url = f'bigquery://{self._gbq_project_id}/{self._dataset}'
    #     return connection_url

    def submit_query(self, query) -> DataFrame:
        return self.submit_queries([query])[0]

    def submit_queries(self, query_list: list) -> list:
        # see: https://pandas-gbq.readthedocs.io/en/latest/reading.html#
        # not using an SQLAlchemy engine or connection for this, but rather using the built
        # in pandas_gbq support.
        import pandas_gbq
        results = []
        for query in query_list:
            results.append(pandas_gbq.read_gbq(
                query, project_id=self.gbq_project_id))
        return results

    def write_df_to_db(self, table_name: str, dataframe: DataFrame,
                       if_exists: PandasTableExistsActionType = PandasTableExistsActionType.FAIL):
        # The code combined sqlalchemy with builtin pandas options if we have pandas_gbq installed.
        # I just went with pandas_gbq approaches direclty on a dataframe and removed sqlalchemy for now.
        # We're only wrapping pandas_gbq methods and not adding anythning here - the only reason to have this
        # is so we can pass in this object to a writeback method, along with a model, to verify the db and tables line up
        # and so that we control the actual table writing and then joining with the model in one method (to ensure those things line up).
        import pandas_gbq
        pandas_gbq.to_gbq(dataframe, f'{self.dataset}.{table_name}',
                          project_id=self.gbq_project_id, if_exists=if_exists.value)

    def execute_statements(self, statements: list):
        #TODO: possibly consider keeping a client around, albeit all the gbq examples I see seem to create them at will and let them be garbage collected
        from google.cloud import bigquery
        client = bigquery.Client(project=self._gbq_project_id)
        client = bigquery.Client()
        for statement in statements:
            query_job = client.query(statement)
            # Waits for job to complete, but currently we do nothing with result
            results = query_job.result()
