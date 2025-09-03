from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query, Path

app = FastAPI()

# Path parameters


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items/{request_id}")
async def read_item(request_id):
    '''
    This request handler will never be reached
    :param request_id:
    :return:
    '''
    return {"request_id": request_id}


# Specified parameters

@app.get("/requests/current")
async def read_item():
    return {"request": "current item"}


@app.get("/requests/{request_id}")
async def read_item(request_id):
    return {"request": request_id}

# Enums as parameters values


class RequestTypes(str, Enum):
    service = 'service'
    new_feature = 'new_feature'


@app.get("/requests/type/{request_type}")
async def read_item(request_type: RequestTypes):
    return {"request_typpe": request_type.value}


# Query string

@app.get("/query_params")
async def read_item(page: int = 0, skip: int = 0):
    return {
        "page": page,
        "skip": skip
    }


@app.get("/query_params")
async def read_item(req: str, page: int = 0, skip: int = 0):
    return {
        "page": page,
        "skip": skip,
        "req": req
    }


@app.get("/query_params_typed")
async def read_item(req: Annotated[str, Query(min_length=5, max_length=15)]):
    return {
        "req": req
    }


@app.get("/items_validated/{request_id}")
async def read_item(request_id: Annotated[int, Path(ge=10, lt=15)]):
    return {"request_id": request_id}
