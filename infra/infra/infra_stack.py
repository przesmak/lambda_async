from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function_handler = _lambda.Function(self, "LambdaAsyncFunction",
                            function_name="lambda-async-dev",
                            runtime=_lambda.Runtime.PYTHON_3_8,
                            code=_lambda.Code.from_asset("asset"),
                            handler="async_handler.handler")
        
        api = apigw.RestApi(
            self,
            "lambda_api",
            rest_api_name="lambda-async-dev_api",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=["*"],
            ),
        )

        get_lambda_integration = apigw.LambdaIntegration(
            function_handler,
            request_templates={"application/json": '{ "statusCode": "200"}'},
        )

        api.root.add_method("POST", get_lambda_integration)
        api.root.add_method("GET", get_lambda_integration)
