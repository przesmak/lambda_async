from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda
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
        