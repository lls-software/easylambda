from os import environ
from random import randint
from secrets import token_hex
from typing import Annotated
from uuid import uuid4

from leandropls.easylambda import get
from leandropls.easylambda.aws import Response
from leandropls.easylambda.query import Query


@get("/")
def lambda_handler(
    hub_mode: Annotated[str, Query("hub.mode")],
    hub_challenge: Annotated[str, Query("hub.challenge")],
    hub_verify_token: Annotated[str, Query("hub.verify_token")],
) -> Response:
    verify_token = environ.get("VERIFY_TOKEN", None)
    if verify_token is None:
        return Response(
            statusCode=500,
            body="VERIFY_TOKEN environment variable is required",
        )
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return Response(
            statusCode=200,
            body=hub_challenge,
        )
    return Response(
        statusCode=403,
        body="Verification failed",
    )


def test_success() -> None:
    hub_challenge = str(randint(100000000, 1000000000))
    hub_verify_token = token_hex()
    environ["VERIFY_TOKEN"] = hub_verify_token
    # noinspection HttpUrlsUsage
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/",
            "rawQueryString": f"hub.mode=subscribe&hub.challenge={hub_challenge}&hub.verify_token={hub_verify_token}",
            "headers": {},
            "queryStringParameters": {
                "hub.mode": "subscribe",
                "hub.verify_token": hub_verify_token,
                "hub.challenge": hub_challenge,
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "domainName": "url-id.lambda-url.us-east-2.on.aws",
                "domainPrefix": "url-id",
                "http": {
                    "method": "GET",
                    "path": "/",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "facebookplatform/1.0 (+http://developers.facebook.com)",
                },
                "requestId": str(uuid4()),
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390,
            },
            "isBase64Encoded": False,
        },
        object(),
    )

    assert response["statusCode"] == 200
    assert response["body"] == hub_challenge


def test_failure() -> None:
    hub_challenge = str(randint(100000000, 1000000000))
    hub_verify_token = token_hex()
    environ["VERIFY_TOKEN"] = "something else"
    # noinspection HttpUrlsUsage
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/",
            "rawQueryString": f"hub.mode=subscribe&hub.challenge={hub_challenge}&hub.verify_token={hub_verify_token}",
            "headers": {},
            "queryStringParameters": {
                "hub.mode": "subscribe",
                "hub.verify_token": hub_verify_token,
                "hub.challenge": hub_challenge,
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "domainName": "url-id.lambda-url.us-east-2.on.aws",
                "domainPrefix": "url-id",
                "http": {
                    "method": "GET",
                    "path": "/",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "facebookplatform/1.0 (+http://developers.facebook.com)",
                },
                "requestId": str(uuid4()),
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390,
            },
            "isBase64Encoded": False,
        },
        object(),
    )

    assert response["statusCode"] == 403
