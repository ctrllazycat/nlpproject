# nlpproject
nlp project using aws

## Lambda Guide:
Create a Reddit App<br>
Go to: https://www.reddit.com/prefs/apps<br>
Click “Create another app…”<br>
Name: lambda-reddit-bot<br>
App type: script<br>
Redirect URI: http://localhost:8080<br>
Save your:<br>
client ID (just under the app name)<br>
client secret<br>
and as User-Agent use "lambda-reddit-bot/0.1 by u/YOUR_USERNAME"<br>
And Upload them to the AWS Secrets Manager<br>

## AWS Glue Guide
Go to AWS GLUE and paste script from glue_spark.py

## Athena Query Guide
Open the query and create new database manually<br>
Copy and paste query from athena_query_create_table.sql

