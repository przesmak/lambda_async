import json
import datetime
import time
import logging
import io
import os
import boto3
from botocore.exceptions import ClientError

S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

logging.basicConfig()
logger = logging.getLogger()


def _sleep_for(max_seconds=10):
    logger.info(f"sleep_start_time:{str(datetime.datetime.now())}")
    time.sleep(max_seconds)
    logger.info(f"sleep_end_time:{str(datetime.datetime.now())}")


def handler(event, context):
    """
    Main function of async invocation

    Lambda waits few seconds before sending response with status code.
    Before execution, JSON with status 'in_progress' is sending to S3 bucket.

    param: event - can be anything
    """

    print("request: {}".format(json.dumps(event)))

    try:
        data = io.BytesIO(json.dumps({"status": "in_progress"}).encode())
        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(data, S3_BUCKET_NAME, 'status')
    except ClientError as exc:
        logger.error(f"Cannot send status in_progress. Error: {exc}")
        raise

    _sleep_for(30)

    response = {"statusCode": 200,
            "status": "done",
            "headers": {}}
    return response
