from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import col
import re

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Your S3 path
input_path = "s3://your-bucket/reddit-data/"

# List all files in the path using boto3
import boto3
s3 = boto3.client("s3")
bucket_name = "your-bucket"
prefix = "reddit-data/"
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# Filter only files matching posts_*.json
files = [
    f"s3://{bucket_name}/{obj['Key']}"
    for obj in response.get("Contents", [])
    if re.match(r".*posts_.*\.json$", obj["Key"])
]

# Load the filtered files
df = spark.read.json(files)

# Optionally do transformations here
df_cleaned = df.select("id", "subreddit", "title")

# Write cleaned data to a new location
df_cleaned.write.mode("overwrite").csv("s3://your-bucket/reddit-cleaned/")
