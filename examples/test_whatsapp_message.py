import hmac
from hashlib import sha256
from secrets import token_hex
from typing import Annotated, Any, Literal, Match
from uuid import uuid4

from pydantic import BaseModel, Field

from leandropls.easylambda import post
from leandropls.easylambda.aws import Event
from leandropls.easylambda.body import Body
from leandropls.easylambda.dependency import Dependency
from leandropls.easylambda.errors import HttpUnauthorized
from leandropls.easylambda.header import Header

APP_SECRET = token_hex(16)


class ContextMessageField(BaseModel):
    forwarded: bool
    frequently_forwarded: bool
    from_: str
    id: str
    referred_product: dict[str, str]


class ErrorMessageField(BaseModel):
    code: int
    title: str
    message: str
    error_data: dict[str, str]


class InteractiveButtonReplyMessageField(BaseModel):
    id: str
    title: str


class InteractiveListReplyMessageField(BaseModel):
    id: str
    title: str
    description: str


class InteractiveMessageField(BaseModel):
    type: InteractiveButtonReplyMessageField | InteractiveListReplyMessageField


class ProductItemField(BaseModel):
    product_retailer_id: str
    quantity: str
    item_price: str
    currency: str


class OrderMessageField(BaseModel):
    catalog_id: str
    text: str
    product_items: list[ProductItemField]


class ReferralMessageField(BaseModel):
    source_url: str
    source_type: str
    source_id: str
    headline: str
    body: str
    media_type: str
    image_url: str
    video_url: str
    thumbnail_url: str
    ctwa_clid: str


class TextMessageField(BaseModel):
    body: str


class IdentityMessageField(BaseModel):
    acknowledged: Any
    created_timestamp: str
    hash: str


class TextMessage(BaseModel):
    context: ContextMessageField | None = None
    errors: list[ErrorMessageField] | None = None
    from_number: Annotated[str, Field(validation_alias="from")]
    id: str
    identity: IdentityMessageField | None = None
    interactive: InteractiveMessageField | None = None
    order: OrderMessageField | None = None
    referral: ReferralMessageField | None = None
    timestamp: str
    type: Literal["text"]
    text: TextMessageField


class Profile(BaseModel):
    name: str


class Contact(BaseModel):
    profile: Profile
    wa_id: str


class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class WhatsAppValue(BaseModel):
    messaging_product: Literal["whatsapp"]
    metadata: Metadata
    contacts: list[Contact]
    messages: list[TextMessage | dict]


class ChangeItem(BaseModel):
    field: Literal["messages"]
    value: WhatsAppValue


class EntryItem(BaseModel):
    id: str
    changes: list[ChangeItem]


class RequestBody(BaseModel):
    object: Literal["whatsapp_business_account"]
    entry: list[EntryItem]


class IsSignatureValid(Dependency):
    __slots__ = ("secret_token",)

    def __init__(self, secret_token: str) -> None:
        self.secret_token = secret_token.encode("utf-8")

    def __call__(self, event: Event, route: Match) -> bool:
        try:
            signature_header = Header("x-hub-signature-256")(event, route)
        except KeyError:
            return False
        expected_signature = (
            f"sha256={hmac.new(self.secret_token, event.body.encode('utf-8'), sha256).hexdigest()}"
        )
        if not hmac.compare_digest(expected_signature, signature_header):
            return False
        return True


@post("/")
def lambda_handler(
    body: Annotated[RequestBody, Body],
    valid_signature: Annotated[bool, IsSignatureValid(APP_SECRET)],
) -> None:
    if not valid_signature:
        raise HttpUnauthorized(message="Invalid signature.")

    for entry in body.entry:
        for change in entry.changes:
            for message in change.value.messages:
                if isinstance(message, TextMessage):
                    # do something
                    ...
                else:
                    continue


def test_success() -> None:
    body = '{"object":"whatsapp_business_account","entry":[{"id":"0","changes":[{"field":"messages","value":{"messaging_product":"whatsapp","metadata":{"display_phone_number":"16505551111","phone_number_id":"123456123"},"contacts":[{"profile":{"name":"test user name"},"wa_id":"16315551181"}],"messages":[{"from":"16315551181","id":"ABGGFlA5Fpa","timestamp":"1504902988","type":"text","text":{"body":"this is a text message"}}]}}]}]}'
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/",
            "rawQueryString": "",
            "cookies": None,
            "headers": {
                "x-hub-signature-256": "sha256="
                + hmac.new(
                    APP_SECRET.encode("utf-8"),
                    msg=body.encode("utf-8"),
                    digestmod=sha256,
                ).hexdigest(),
                "content-type": "application/json",
            },
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "anonymous",
                "apiId": "url-id",
                "authentication": None,
                "authorizer": None,
                "domainName": "url-id.lambda-url.us-east-2.on.aws",
                "domainPrefix": "url-id",
                "http": {
                    "method": "POST",
                    "path": "/",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "facebookexternalua",
                },
                "requestId": str(uuid4()),
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390,
            },
            "body": body,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None,
            "urlMatch": {},
        },
        object(),
    )
    assert response["statusCode"] == 204


def test_signature_failure() -> None:
    body = '{"object":"whatsapp_business_account","entry":[{"id":"0","changes":[{"field":"messages","value":{"messaging_product":"whatsapp","metadata":{"display_phone_number":"16505551111","phone_number_id":"123456123"},"contacts":[{"profile":{"name":"test user name"},"wa_id":"16315551181"}],"messages":[{"from":"16315551181","id":"ABGGFlA5Fpa","timestamp":"1504902988","type":"text","text":{"body":"this is a text message"}}]}}]}]}'
    response = lambda_handler(
        {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/",
            "rawQueryString": "",
            "cookies": None,
            "headers": {
                "x-hub-signature-256": "sha256="
                + hmac.new(
                    token_hex(16).encode("utf-8"),
                    msg=body.encode("utf-8"),
                    digestmod=sha256,
                ).hexdigest(),
                "content-type": "application/json",
            },
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "anonymous",
                "apiId": "url-id",
                "authentication": None,
                "authorizer": None,
                "domainName": "url-id.lambda-url.us-east-2.on.aws",
                "domainPrefix": "url-id",
                "http": {
                    "method": "POST",
                    "path": "/",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "facebookexternalua",
                },
                "requestId": str(uuid4()),
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390,
            },
            "body": body,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None,
            "urlMatch": {},
        },
        object(),
    )
    assert response["statusCode"] == 401
