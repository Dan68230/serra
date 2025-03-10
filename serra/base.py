from abc import ABC, abstractmethod
from serra.profile import SerraProfile

class Step(ABC):
    # @abstractmethod
    # def execute(self, **args):
    #     pass

    def add_serra_profile(self, serra_profile: SerraProfile):
        self.serra_profile = serra_profile

    def add_spark_session(self, spark):
        self.spark = spark