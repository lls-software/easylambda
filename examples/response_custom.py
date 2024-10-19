from easylambda import get
from easylambda.aws import Response


@get("/")
def lambda_handler() -> Response:
    return Response(
        statusCode=418,
        body="I'm a teapot",
    )
