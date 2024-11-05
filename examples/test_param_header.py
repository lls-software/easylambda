import json
from typing import Annotated

from leandropls.easylambda import get
from leandropls.easylambda.header import Header


@get("/items")
def lambda_handler(
    user_agent: Annotated[str | None, Header("user-agent")] = None,
) -> dict:
    return {"User-Agent": user_agent}


def test_present() -> None:
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/items",
            "rawQueryString": "",
            "cookies": [],
            "headers": {
                "user-agent": "agent",
            },
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
                    "path": "/items",
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
    assert json.loads(response["body"]) == {"User-Agent": "agent"}


def test_not_present() -> None:
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/items",
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
                    "path": "/items",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "",
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
    assert json.loads(response["body"]) == {"User-Agent": None}
