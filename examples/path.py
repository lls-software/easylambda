from typing import Annotated

from easylambda import get
from easylambda.path import Path


@get("/items/{item_id}")
def lambda_handler(item_id: Annotated[int, Path("item_id")]) -> dict:
    return {"item_id": item_id}
