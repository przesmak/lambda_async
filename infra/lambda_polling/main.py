import logging
import boto3
import json
import os
from botocore.exceptions import ClientError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


def handler(event, context):
    logger.info(json.dumps(event))

    try:
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key='status')
        logger.info(response)
        obj = json.loads(response.get("Body").read().decode('utf-8'))
        logger.info(obj.get('status'))
        if obj.get('status') == 'done':
            return {"statusCode": 200,
                    "body": "Job is finished",
                    "headers": {}}
    except ClientError as exc:
        logger.warning(f"Cannot save the file with status. Error: {exc}")

    return {"statusCode": 200,
        "body": "Event in progress",
        "headers": {}}

