import unittest
from pyspark.sql import SparkSession
import glob
import os

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # jarDependencies = glob.glob("/opt/docker/lib/*.jar")
        sparkSession = (
            SparkSession.builder.master("local")
            .appName("init")
            .config("spark.sql.legacy.allowUntypedScalaUDF", "true")
            .config("spark.port.maxRetries", "100")
        )

        jars = os.getenv('SPARK_JARS_CONFIG')

        #jars = "/Users/abhishek/alternate_repo/prophecy-libs/target/scala-2.12/prophecy-libs-assembly-3.4.0-7.1.9-SNAPSHOT.jar"

        fallBackSparkPackages = [
            "io.prophecy:prophecy-libs_2.12:6.3.0-3.1.2"
        ]

        if (jars and jars!=""):
            sparkSessionWithReqdDependencies = sparkSession.config("spark.jars", jars)
        else:
            sparkSessionWithReqdDependencies = sparkSession.config("spark.jars.packages",
                                                                   ",".join(fallBackSparkPackages))

        cls.spark = (sparkSessionWithReqdDependencies.getOrCreate())
        cls.maxUnequalRowsToShow = 5

    def setup(self):
        self.spark = BaseTestCase.spark
        self.maxUnequalRowsToShow = BaseTestCase.maxUnequalRowsToShow
