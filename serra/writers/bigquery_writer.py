from google.cloud import bigquery
import os

from serra.exceptions import SerraRunException
from serra.writers import Writer

class BigQueryWriter(Writer):
    """
    A reader to write data to BigQuery from a Spark DataFrame.

    :param config: A dictionary containing the configuration for the reader.
                   It should have the following keys:
                   - 'project'
                   - 'dataset'
                   - 'table'
    """

    def __init__(self, project, dataset, table, mode):
        self.project = project
        self.dataset = dataset
        self.table = table
        self.mode = mode

    @classmethod
    def from_config(cls, config):
        project = config.get('project')
        dataset = config.get('dataset')
        table = config.get('table')
        mode = config.get('mode')

        obj = cls(project, dataset, table, mode)
        obj.input_block = config.get('input_block')
        return obj

    def write(self, df):
        """
        Read data from Snowflake and return a Spark DataFrame.

        :return: A Spark DataFrame containing the data read from the specified Snowflake table.
        """
        pandas_df = df.toPandas()
        bigquery_account_json_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not bigquery_account_json_path:
            raise SerraRunException("Please set environment variable GOOGLE_APPLICATION_CREDENTIALS to path to Google Cloud Service Account")
        client = bigquery.Client.from_service_account_json(bigquery_account_json_path)
        # Query to fetch data
        table_ref = f"{self.project}.{self.dataset}.{self.table}"

        # Write pandas DataFrame to BigQuery table
        job_config = bigquery.LoadJobConfig()
        if self.mode == "append":
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        elif self.mode == "overwrite":
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        elif self.mode == "error":
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
        job = client.load_table_from_dataframe(pandas_df, table_ref, job_config=job_config)
        job.result()  # Wait for the job to complete