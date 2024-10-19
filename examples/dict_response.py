from easylambda import get


@get("/")
def lambda_handler() -> dict:
    return {"message": "Hello World!"}
