#!/usr/bin/env python

import json
import os
from functools import cache
from typing import Any

import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
tracer = Tracer()


@cache
def _instantiate_dynamodb_table() -> Any:
    """Instantiate a DynamoDB table resource.

    Returns:
        Any: DynamoDB Table resource.

    """
    table_name = os.environ["DYNAMODB_TABLE_NAME"]
    return boto3.resource("dynamodb").Table(table_name)


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:  # noqa: ARG001
    """AWS Lambda function handler.

    This function handles media stream requests.

    Args:
        event (dict[str, Any]): The event data passed by AWS Lambda.
        context (LambdaContext): The runtime information provided by AWS Lambda.

    Returns:
        dict[str, Any]: A dictionary representing the API Gateway response.

    """
    endpoint_url = "https://{d}/{s}".format(d=event["domain"], s=event["stage"])
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Endpoint URL: {endpoint_url}"}),
    }