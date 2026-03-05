"""PySpark batch transform for large-volume metric ingestion."""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, dayofweek, hour, to_timestamp


def run_spark_transform(input_csv: str, output_parquet: str) -> None:
    spark = SparkSession.builder.appName("metric-anomaly-prep").getOrCreate()

    df = spark.read.option("header", True).csv(input_csv)
    out = (
        df.withColumn("timestamp", to_timestamp(col("timestamp")))
        .withColumn("value", col("value").cast("double"))
        .withColumn("hour", hour(col("timestamp")))
        .withColumn("dayofweek", dayofweek(col("timestamp")))
    )

    out.write.mode("overwrite").parquet(output_parquet)
    spark.stop()


if __name__ == "__main__":
    run_spark_transform("data/raw/business_metrics.csv", "data/processed/business_metrics.parquet")