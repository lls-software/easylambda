import json
from typing import Annotated

from easylambda import get
from easylambda.path import Path


@get("/items/{item_id}")
def lambda_handler(item_id: Annotated[int, Path("item_id")]) -> dict:
    return {"item_id": item_id}


def test_success() -> None:
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/items/123",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {},
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": None,
                "domainName": "url-id.lambda-url.us-west-2.on.aws",
                "domainPrefix": "url-id",
                "http": {
                    "method": "GET",
                    "path": "/items/123",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent",
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390,
            },
            "body": "",
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None,
        },
        object(),
    )

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"item_id": 123}


def test_invalid_id() -> None:
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/items/word",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {},
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": None,
                "domainName": "url-id.lambda-url.us-west-2.on.aws",
                "domainPrefix": "url-id",
                "http": {
                    "method": "GET",
                    "path": "/items/word",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent",
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390,
            },
            "body": "",
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None,
        },
        object(),
    )

    assert response["statusCode"] == 422
