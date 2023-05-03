#!/usr/bin/env python3
import aws_cdk as cdk

from lambda_bootstrap.lambda_bootstrap_stack import LambdaBootstrapStack

app = cdk.App()
LambdaBootstrapStack(app, "LambdaBootstrapStack")

app.synth()
