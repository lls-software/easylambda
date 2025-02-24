import json
from typing import Annotated

from easylambda import get
from easylambda.query import Query

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@get("/items")
def lambda_handler(
    skip: Annotated[int, Query("skip")] = 0,
    limit: Annotated[int, Query("limit")] = 10,
) -> list[dict]:
    return fake_items_db[skip : skip + limit]


def test_success() -> None:
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/items",
            "rawQueryString": "skip=1&limit=1",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {"skip": "1", "limit": "1"},
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
    assert json.loads(response["body"]) == [{"item_name": "Bar"}]


def test_invalid_parameter() -> None:
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/items",
            "rawQueryString": "skip=1&limit=word",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {"skip": "1", "limit": "word"},
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

    assert response["statusCode"] == 422
