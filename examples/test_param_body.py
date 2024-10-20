from typing import Annotated

from easylambda import post
from easylambda.body import Body
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@post("/items")
def lambda_handler(item: Annotated[Item, Body]) -> dict:
    return item.model_dump()
