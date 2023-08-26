import logging
from atscale.atscale import AtScale
from atscale.db.bigquery import BigQuery
from atscale.db.databricks import Databricks
from atscale.db.iris import Iris
from atscale.db.redshift import Redshift
from atscale.db.snowflake import Snowflake
from atscale.db.synapse import Synapse

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.WARNING,
)