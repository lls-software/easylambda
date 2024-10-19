from typing import Any
from urllib.parse import parse_qs

from pydantic import BaseModel, ConfigDict


class Validity(BaseModel):
    notBefore: str
    notAfter: str


class ClientCert(BaseModel):
    clientCertPem: str
    subjectDN: str
    issuerDN: str
    serialNumber: str
    validity: Validity


class Authentication(BaseModel):
    clientCert: ClientCert


class Jwt(BaseModel):
    claims: dict[str, Any]
    scopes: list[str]


class Authorizer(BaseModel):
    jwt: Jwt


class Http(BaseModel):
    method: str
    path: str
    protocol: str
    sourceIp: str
    userAgent: str


class RequestContext(BaseModel):
    accountId: str
    apiId: str
    authentication: Authentication | None = None
    authorizer: Authorizer | None = None
    domainName: str
    domainPrefix: str
    http: Http
    requestId: str
    routeKey: str
    stage: str
    time: str
    timeEpoch: int


class Event(BaseModel):
    version: str
    routeKey: str
    rawPath: str
    rawQueryString: str
    cookies: list[str] | None = None
    headers: dict[str, str]
    queryStringParameters: dict[str, str] | None = None
    requestContext: RequestContext
    body: str | None = None
    pathParameters: dict[str, str] | None = None
    isBase64Encoded: bool
    stageVariables: dict[str, str] | None = None
    urlMatch: dict[str, str] = {}

    model_config = ConfigDict(frozen=True)

    _parse_qs_cache = None
    _parse_qs_cache_valid = False

    def parse_qs(self) -> dict[str, list[str]]:
        if self._parse_qs_cache_valid is False:
            self._parse_qs_cache = parse_qs(self.rawQueryString)
            self._parse_qs_cache_valid = True
        return self._parse_qs_cache

    @property
    def content_type(self) -> str | None:
        return self.headers.get("content-type", None)


class Response(BaseModel):
    statusCode: int
    headers: dict[str, str] | None = None
    isBase64Encoded: bool = False
    multiValueHeaders: dict[str, list[str]] = {}
    body: str = ""
