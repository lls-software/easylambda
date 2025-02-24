import json

from easylambda.method_router import MethodRouter

lambda_handler = MethodRouter("/")


@lambda_handler.get
def get_handler() -> dict:
    return {"method": "GET"}


@lambda_handler.post
def post_handler() -> dict:
    return {"method": "POST"}


def test_get() -> None:
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/",
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
                    "path": "/",
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
    assert json.loads(response["body"]) == {"method": "GET"}


def test_post() -> None:
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/",
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
                    "method": "POST",
                    "path": "/",
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
    assert json.loads(response["body"]) == {"method": "POST"}
