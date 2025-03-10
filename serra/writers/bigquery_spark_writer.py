from google.cloud import bigquery

from serra.exceptions import SerraRunException
from serra.writers import Writer

class BigQueryWriter(Writer):
    """
    A reader to write data to BigQuery from a Spark DataFrame.

    :param config: A dictionary containing the configuration for the reader.
                   It should have the following keys:
                   - 'project_id'
                   - 'dataset_id'
                   - 'table_id'
    """

    def __init__(self, project_id, dataset_id, table_id, mode):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.mode = mode

    @classmethod
    def from_config(cls, config):
        project_id = config.get('project_id')
        dataset_id = config.get('dataset_id')
        table_id = config.get('table_id')
        mode = config.get('mode')

        obj = cls(project_id, dataset_id, table_id, mode)
        obj.input_block = config.get('input_block')
        return obj
    
    def write(self, df):
        """
        Read data from Snowflake and return a Spark DataFrame.

        :return: A Spark DataFrame containing the data read from the specified Snowflake table.
        """
        df.write \
            .format("bigquery") \
            .option('project', self.project_id)\
            .option("writeMethod", "direct") \
            .mode(self.mode)\
            .save(f"{self.dataset_id}.{self.table_id}")
