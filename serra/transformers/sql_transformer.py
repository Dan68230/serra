from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from serra.transformers.transformer import Transformer

class SQLTransformer(Transformer):
    """
    A transformer to perform a SQL SELECT operation on a DataFrame.

    :param sql_expression: A SQL expression string representing the SELECT operation.
    """

    def __init__(self, sql_expression):
        self.sql_expression = sql_expression

    @classmethod
    def from_config(cls, config):
        sql_expression = config.get('sql_expression')

        obj = cls(sql_expression)
        obj.input_block = config.get('input_block')
        return obj

    def transform(self, df: DataFrame) -> DataFrame:
        """
        Perform the SELECT operation on the DataFrame.

        :param df: The input DataFrame to be transformed.
        :return: A new DataFrame containing only the selected columns.
        :raises: SerraRunException if no columns are specified in the configuration
                 or if none of the specified columns exist in the DataFrame.
        """
        df = df.filter(F.expr(self.sql_expression))
        return df



