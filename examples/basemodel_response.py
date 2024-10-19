from easylambda import get
from pydantic import BaseModel


class HandlerResponse(BaseModel):
    message: str


@get("/")
def lambda_handler() -> HandlerResponse:
    return HandlerResponse(message="Hello World!")
