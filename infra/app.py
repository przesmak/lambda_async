#!/usr/bin/env python3
import aws_cdk as cdk

from infra.infra_stack import InfraStack


app = cdk.App()
InfraStack(app, "InfraStack",
    stack_name="lambda-async-test")

app.synth()
