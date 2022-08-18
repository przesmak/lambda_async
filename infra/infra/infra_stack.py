from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_lambda_destinations as destinations,
    aws_apigateway as apigw,
    aws_s3 as s3,
)
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Main document storage
        s3_data = s3.Bucket(self, "DocumentBucket", bucket_name="lambda-async-dev-documents")

        # Lambdas definition
        main_handler = _lambda.Function(self, "LambdaAsyncFunction",
                            function_name="lambda-async-dev",
                            runtime=_lambda.Runtime.PYTHON_3_8,
                            code=_lambda.Code.from_asset("asset"),
                            handler="async_handler.handler",
                            timeout=Duration.minutes(15),
                            environment={"S3_BUCKET_NAME": s3_data.bucket_name})

        function_on_success = _lambda.Function(self, "SuccessHandler",
                            function_name="lambda-async-dev-onsuccess",
                            runtime=_lambda.Runtime.PYTHON_3_8,
                            code=_lambda.Code.from_asset("on_success"),
                            handler="main.handler",
                            environment={"S3_BUCKET_NAME": s3_data.bucket_name})

        polling_handler = _lambda.Function(self, "PollingHandler",
                            function_name="lambda-async-dev-polling",
                            runtime=_lambda.Runtime.PYTHON_3_8,
                            code=_lambda.Code.from_asset("lambda_polling"),
                            handler="main.handler",
                            environment={"S3_BUCKET_NAME": s3_data.bucket_name})

        # policy for S3 bucket
        s3_data.grant_write(function_on_success)
        s3_data.grant_read(polling_handler)
        s3_data.grant_write(main_handler)

        # Invoke policy on success
        function_on_success.grant_invoke(main_handler)

        # Main lambda invocation strategy
        _lambda.EventInvokeConfig(self, "EventInvokeLambda", function=main_handler,
                                on_success=destinations.LambdaDestination(function_on_success, response_only=True),
                                on_failure=destinations.LambdaDestination(function_on_success, response_only=True))

        # Add API GW front end for the Lambda
        api_stage_options = apigw.StageOptions(
            stage_name="api_stage_async",
            throttling_rate_limit=10,
            throttling_burst_limit=100,
            logging_level=apigw.MethodLoggingLevel.INFO
        )

        api = apigw.RestApi(
            self,
            "lambda_api",
            rest_api_name="lambda-async-dev_api",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=["*"],
            ),
            deploy_options=api_stage_options
        )

        resp_template = """{
        #foreach($param in $input.params().header.keySet())
        #if($param == "invocationtype" or $param == "InvocationType" && $util.escapeJavaScript($input.params().header.get($param)) == "Event")
        #set($is_async = "true")
        #end
        #end
        #if($is_async == "true")
        "asynchronous_invocation":"true",
        "message":"Event received. Check queue/logs for status"
        #else
        "synchronous_invocation":"true",
        #end
        }
        """

        post_lambda_integration = apigw.LambdaIntegration(
            main_handler,
            proxy=False,
            passthrough_behavior=apigw.PassthroughBehavior.WHEN_NO_TEMPLATES,
            request_templates={"application/json": '{ "statusCode": "200"}'},
            request_parameters={"integration.request.header.X-Amz-Invocation-Type": "method.request.path.InvocationType"},
            integration_responses=[apigw.IntegrationResponse(status_code="200",
                    response_parameters={

                    }, response_templates={
                        "application/json": f"{resp_template}"})
            ]
        )

        get_lambda_integration = apigw.LambdaIntegration(
            polling_handler,
            request_templates={"application/json": '{ "statusCode": "200"}'},
        )

        api.root.add_method(http_method="POST",
                        integration=post_lambda_integration,
                        request_parameters={
                            "method.request.header.InvocationType": True
                        }, method_responses=[
                            apigw.MethodResponse(status_code="200",
                            response_parameters={
                                "method.response.header.Content-Length": True,
                            }, response_models={
                                "application/json": apigw.Model.EMPTY_MODEL
                            })
                        ])

        api.root.add_method(http_method="GET", integration=get_lambda_integration)
