import os

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigateway as apigw,
)

from constructs import Construct


class LambdaBootstrapStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM role with relevant permissions
        role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        # Lambda function with outgoing HTTP request
        healthcheck_function = _lambda.Function(
            self, "GoHealthcheckLambda",
            code=_lambda.Code.from_asset("lambda"),
            handler="main",
            runtime=_lambda.Runtime.GO_1_X
            role=role,
            memorySize: 128,
            timeout: Duration.seconds(10),
        )

        # API Gateway without IAM authentication
        api = apigw.LambdaRestApi(
            self, "healthcheckApi",
            handler=healthcheck_function,
            proxy=True
        )

        # Define the root resource
        root_resource = api.root

        # Add a GET method to the root resource
        root_resource.add_method("POST", api_key_required=False)
