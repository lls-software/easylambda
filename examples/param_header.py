from typing import Annotated

from easylambda import get
from easylambda.header import Header


@get("/items")
def lambda_handler(
    user_agent: Annotated[str | None, Header("user-agent")] = None,
) -> dict:
    return {"User-Agent": user_agent}
