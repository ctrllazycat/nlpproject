import praw
import boto3
import json
from datetime import datetime
import os

S3_BUCKET = os.getenv("S3_BUCKET", "s3-bucket-name") # use your own bucket name
SEEN_IDS_KEY = "reddit-data/seen_ids.json"
SUBREDDITS = ["TheOnion", "Conspiracy"]
SECRETS_NAME = os.getenv("REDDIT_SECRET_NAME", "reddit/api/creds")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def get_reddit_secrets(secret_name=SECRETS_NAME, region_name=AWS_REGION):
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def load_seen_ids(s3):
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=SEEN_IDS_KEY)
        seen_ids = json.loads(obj["Body"].read())
        return set(seen_ids)
    except s3.exceptions.NoSuchKey:
        print(f"No previous seen_ids found at {SEEN_IDS_KEY}, starting fresh.")
        return set()
    except Exception as e:
        print(f"Error loading seen_ids: {e}")
        return set()

def save_seen_ids(s3, seen_ids):
    try:
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=SEEN_IDS_KEY,
            Body=json.dumps(list(seen_ids)),
            ContentType="application/json"
        )
        print(f"Seen IDs saved to {SEEN_IDS_KEY}")
    except Exception as e:
        print(f"Failed to save seen_ids: {e}")

def lambda_handler(event, context):
    creds = get_reddit_secrets()

    # Setup Reddit client
    reddit = praw.Reddit(
        client_id=creds["REDDIT_CLIENT_ID"],
        client_secret=creds["REDDIT_CLIENT_SECRET"],
        user_agent=creds["REDDIT_USER_AGENT"],
    )

    s3 = boto3.client("s3")
    seen_ids = load_seen_ids(s3)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    new_total = 0

    for sub in SUBREDDITS:
        new_posts = []
        subreddit = reddit.subreddit(sub)

        for submission in subreddit.new(limit=50):
            if submission.id not in seen_ids:
                new_posts.append({
                    "id": submission.id,
                    "subreddit": sub,
                    "title": submission.title,
                    "score": submission.score,
                    "url": submission.url,
                    "created_utc": submission.created_utc,
                    "num_comments": submission.num_comments,
                    "author": str(submission.author)
                })
                seen_ids.add(submission.id)

        if new_posts:
            key = f"reddit-data/{sub}/posts_{timestamp}.json"
            try:
                s3.put_object(
                    Bucket=S3_BUCKET,
                    Key=key,
                    Body=json.dumps(new_posts),
                    ContentType="application/json"
                )
                print(f"✅ Saved {len(new_posts)} posts from r/{sub} to {key}")
                new_total += len(new_posts)
            except Exception as e:
                print(f"❌ Failed to upload posts to S3: {e}")

    save_seen_ids(s3, seen_ids)

    return {
        "statusCode": 200,
        "body": f"Saved {new_total} total new posts"
    }
