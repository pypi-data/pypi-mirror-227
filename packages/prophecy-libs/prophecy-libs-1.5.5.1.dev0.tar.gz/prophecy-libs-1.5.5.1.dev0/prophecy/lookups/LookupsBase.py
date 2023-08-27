# WARNING - Do not add import * in this module

from typing import List, Optional

from pyspark.sql import SparkSession
from pyspark.sql.column import Column
from pyspark.sql.functions import DataFrame


class LookupsBase:
    sparkSession = None
    UDFUtils = None

    def __init__(self, spark):
        self.UDFUtils = spark.sparkContext._jvm.io.prophecy.libs.python.UDFUtils
        self.sparkSession = spark


lookupConfig: Optional[LookupsBase] = None


class Condition:
    lookupColumn = ""
    comparisonOp = ""
    def __init__(self, lookupColumn, camparisonOp):
        self.lookupColumn = lookupColumn
        self.comparisonOp = camparisonOp


def initializeLookups(spark):
    global lookupConfig
    if lookupConfig is None:
        lookupConfig = LookupsBase(spark)
    return lookupConfig


def createScalaList(_list, spark):
    return spark.sparkContext._jvm.PythonUtils.toList(_list)


def createLookup(
        name: str,
        df: DataFrame,
        spark: SparkSession,
        keyCols: List[str],
        valueCols: List[str],
):
    initializeLookups(spark)
    keyColumns = createScalaList(keyCols, spark)
    valueColumns = createScalaList(valueCols, spark)

    lookupConfig.UDFUtils.createLookup(
        name, df._jdf, spark._jsparkSession, keyColumns, valueColumns
    )


def createRangeLookup(
        name: str,
        df: DataFrame,
        spark: SparkSession,
        minColumn: str,
        maxColumn: str,
        valueColumns: List[str],
):
    valueColumns = createScalaList(valueColumns, spark)
    lookupConfig.UDFUtils.createRangeLookup(
        name, df._jdf, spark._jsparkSession, minColumn, maxColumn, valueColumns
    )


def createScalaConditionsList(conditions: List[Condition], spark):
    scalaConditions = []
    for condition in conditions:
        sConditions = lookupConfig.UDFUtils.Condition(condition.lookupColumn, condition.comparisonOp)
        scalaConditions.append(sConditions)
    return spark.sparkContext._jvm.PythonUtils.toList(scalaConditions)


def createExtendedLookup(
        name: str,
        df: DataFrame,
        spark: SparkSession,
        conditions: List[Condition],
        valueColumns: List[str],
):
    initializeLookups(spark)
    conditions = createScalaConditionsList(conditions, spark)
    valueColumns = createScalaList(valueColumns, spark)

    lookupConfig.UDFUtils.createExtendedLookup(
        name, df._jdf, spark._jsparkSession, conditions, valueColumns
    )



def lookup(lookupName: str, *cols):
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup(lookupName, _cols)
    return Column(lookupResult)


def lookup_last(lookupName: str, *cols):
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_last(lookupName, _cols)
    return Column(lookupResult)


def lookup_match(lookupName: str, *cols):
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_match(lookupName, _cols)
    return Column(lookupResult)


def lookup_count(lookupName: str, *cols):
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_count(lookupName, _cols)
    return Column(lookupResult)


def lookup_row(lookupName: str, *cols):
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_row(lookupName, _cols)
    return Column(lookupResult)


def lookup_row_reverse(lookupName: str, *cols):
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_row_reverse(lookupName, _cols)
    return Column(lookupResult)


def lookup_nth(lookupName: str, *cols):
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_nth(lookupName, _cols)
    return Column(lookupResult)
