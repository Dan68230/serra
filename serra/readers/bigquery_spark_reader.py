from serra.readers import Reader


class BigQueryReader(Reader):
    """
    A reader to read data from Snowflake into a Spark DataFrame.

    :param config: A dictionary containing the configuration for the reader.
                   It should have the following keys:
                   - 'project_id'
                   - 'dataset_id'
                   - 'table_id'
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
        return obj

    def read(self):
        """
        Read data from Snowflake and return a Spark DataFrame.

        :return: A Spark DataFrame containing the data read from the specified Snowflake table.
        """
        df = self.spark.read.format("bigquery")\
            .option('parentProject', self.project)\
            .load(f"{self.dataset}.{self.table}")
        return df
    
    def read_with_spark(self, spark):
        self.spark = spark
        return self.read()
