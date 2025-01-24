from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

def create_spark_session():
    return SparkSession.builder \
        .appName("TopKSongs") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

def create_kafka_read_stream(spark, kafka_bootstrap_servers, topic):
    return spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", topic) \
        .load()

def process_stream(df):
    # Define schema for song events
    schema = StructType([
        StructField("song_id", IntegerType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("duration", IntegerType(), True)
    ])
    
    # Parse JSON and calculate top K songs
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    return parsed_df \
        .groupBy("song_id") \
        .agg(count("*").alias("play_count")) \
        .orderBy(desc("play_count")) \
        .limit(10)

def start_streaming():
    time.sleep(100)
    spark = create_spark_session()
    kafka_bootstrap_servers = "kafka:9092"
    topic = "song-events"
    
    streaming_df = create_kafka_read_stream(spark, kafka_bootstrap_servers, topic)
    
    # Process stream and write to console for testing
    query = process_stream(streaming_df) \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()
    
    query.awaitTermination()

if __name__ == "__main__":
    start_streaming()