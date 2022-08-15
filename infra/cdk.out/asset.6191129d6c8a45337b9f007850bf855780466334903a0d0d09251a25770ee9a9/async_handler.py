from asyncio.log import logger
import json 
import datetime
import time
import logging

logging.basicConfig()
logger = logging.getLogger()


def _sleep_for(max_seconds=10):
    logger.info(f"sleep_start_time:{str(datetime.datetime.now())}")
    time.sleep(max_seconds)
    logger.info(f"sleep_end_time:{str(datetime.datetime.now())}")


def handler(event, context):
    print("request: {}".format(json.dumps(event)))
    
    _sleep_for(3)

    response = {"statusCode": 200,
            "body": "wszystko ok",
            "headers": {}}
    return response
