# EasyLambda

A lightweight, FastAPI-inspired framework for building AWS Lambda functions with Python.

## Installation

You can install the library using pip:

```bash
pip install leandropls.easylambda
```

The library is also available as AWS Lambda Layers (choose based on your Python
version and architecture):

- `arn:aws:lambda:us-east-2:144273415340:layer:easylambda-0_1_3-python3_11-arm64:1`
- `arn:aws:lambda:us-east-2:144273415340:layer:easylambda-0_1_3-python3_11-x86_64:1`
- `arn:aws:lambda:us-east-2:144273415340:layer:easylambda-0_1_3-python3_12-arm64:1`
- `arn:aws:lambda:us-east-2:144273415340:layer:easylambda-0_1_3-python3_12-x86_64:1`

Requirements:
- Python 3.11 or 3.12
- AWS Lambda arm64 or x86_64 architecture (when using as a Lambda Layer)
- Region: us-east-2 (when using as a Lambda Layer)

## Quick Start

```python
from leandropls.easylambda import get

@get("/")
def lambda_handler() -> dict:
    return {"message": "Hello World!"}
```

## Features

### Request Parameters

EasyLambda supports various ways to handle request parameters:

#### Path Parameters

```python
from typing import Annotated
from leandropls.easylambda import get
from leandropls.easylambda.path import Path

@get("/items/{item_id}")
def lambda_handler(item_id: Annotated[int, Path("item_id")]) -> dict:
    return {"item_id": item_id}
```

#### Query Parameters

```python
from typing import Annotated
from leandropls.easylambda import get
from leandropls.easylambda.query import Query

items = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@get("/items")
def lambda_handler(
    skip: Annotated[int, Query("skip")] = 0,
    limit: Annotated[int, Query("limit")] = 10,
) -> list[dict]:
    return items[skip : skip + limit]
```

#### Request Body

```python
from typing import Annotated
from leandropls.easylambda import post
from leandropls.easylambda.body import Body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@post("/items")
def lambda_handler(item: Annotated[Item, Body]) -> dict:
    return item.model_dump()
```

#### Headers

```python
from typing import Annotated
from leandropls.easylambda import get
from leandropls.easylambda.header import Header

@get("/items")
def lambda_handler(
    user_agent: Annotated[str | None, Header("user-agent")] = None,
) -> dict:
    return {"User-Agent": user_agent}
```

### Response Handling

EasyLambda provides flexible response handling options:

#### Dictionary Response

The simplest way to return a response:

```python
from leandropls.easylambda import get

@get("/")
def lambda_handler() -> dict:
    return {"message": "Hello World!"}
```

#### Pydantic Model Response

For type-safe responses:

```python
from leandropls.easylambda import get
from pydantic import BaseModel

class HandlerResponse(BaseModel):
    message: str

@get("/")
def lambda_handler() -> HandlerResponse:
    return HandlerResponse(message="Hello World!")
```

#### Custom Response

For full control over the response:

```python
from leandropls.easylambda import get
from leandropls.easylambda.aws import Response

@get("/")
def lambda_handler() -> Response:
    return Response(
        statusCode=418,
        body="I'm a teapot",
    )
```

## Key Features

- FastAPI-inspired syntax
- Type hints and validation using Pydantic
- Support for path parameters, query parameters, request body, and headers
- Flexible response handling
- Lightweight and optimized for AWS Lambda environment
- No heavy web framework dependencies

## Best Practices

1. Use type hints consistently for better code clarity and automatic validation
2. Leverage Pydantic models for request/response validation
3. Keep functions focused and single-purpose
4. Use meaningful parameter names that match your API design
5. Provide default values for optional parameters

## Limitations

- When using as a Lambda Layer:
  - Only available in us-east-2 region
  - Requires Python 3.11 or 3.12
  - Must be used as a Lambda Layer

## Contributing

The project is available on GitHub at: https://github.com/leandropls/easylambda