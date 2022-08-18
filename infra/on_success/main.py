import json
import boto3
from botocore.exceptions import ClientError
import os
import io
import logging

logging.basicConfig()
logger = logging.getLogger()

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


def handler(event, context):
    print("request: {}".format(json.dumps(event)))

    try:
        data = io.BytesIO(json.dumps(event).encode())
        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(data, S3_BUCKET_NAME, 'status')
    except ClientError as exc:
        logger.warning(f"Cannot save the file with status. Error: {exc}")

    return {
        "statusCode": 200,
        "body": "git",
        "headers": {}
    }
