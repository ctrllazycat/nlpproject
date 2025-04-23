# nlpproject
nlp project using aws

## Lambda Guide:
1. Create a Reddit App
Go to: https://www.reddit.com/prefs/apps

Click “Create another app…”

Name: lambda-reddit-bot
App type: script
Redirect URI: http://localhost:8080
Save your:
client ID (just under the app name)
client secret 
and as User-Agent use "lambda-reddit-bot/0.1 by u/YOUR_USERNAME"

And Upload them to the AWS Secrets Manager

## AWS Glue Guide
Go to AWS GLUE and paste script from glue_spark.py

## Athena Query Guide
Open the query and create new database manually
Copy and paste query from athena_query_create_table.sql

