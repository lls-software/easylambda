import json

from pydantic import BaseModel

from leandropls.easylambda import get


class HandlerResponse(BaseModel):
    message: str


@get("/")
def lambda_handler() -> HandlerResponse:
    return HandlerResponse(message="Hello World!")


def test_success() -> None:
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
    assert response["headers"]["Content-Type"] == "application/json"
    assert json.loads(response["body"]) == {"message": "Hello World!"}
