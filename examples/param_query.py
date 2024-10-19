from typing import Annotated

from easylambda import get
from easylambda.query import Query

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@get("/items/")
def lambda_handler(
    skip: Annotated[int, Query("skip")] = 0,
    limit: Annotated[int, Query("limit")] = 10,
) -> list[dict]:
    return fake_items_db[skip : skip + limit]
