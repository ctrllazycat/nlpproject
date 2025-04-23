CREATE EXTERNAL TABLE reddit_cleaned (
  junk STRING,
  id STRING,
  subreddit STRING,
  title STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION 's3://your-s3-bucket-name/reddit-cleaned/'
TBLPROPERTIES ('skip.header.line.count'='1');
