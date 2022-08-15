import json
# import boto3
import os

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


def handler(event, context):
    print("request: {}".format(json.dumps(event)))

    # s3_client = boto3.client('s3')
    return {
        "statusCode": 200,
        "body": "git",
        "headers": {}
    }
