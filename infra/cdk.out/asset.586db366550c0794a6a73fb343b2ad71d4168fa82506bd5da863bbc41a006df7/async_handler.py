import json 


def handler(event, context):
    print("request: {}".format(json.dumps(event)))

    response = {"statusCode": 200,
            "body": "wszystko ok",
            "headers": {}}
    return response
