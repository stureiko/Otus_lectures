from fastapi import FastAPI, Query, Path, Request, Form, File
import uvicorn
from enum import Enum
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
async def get_root():
    return {'message': 'Hello'}

# * * * * * * * * * * * 
# Path parameters

@app.get('/items')
async def get_all_items():
    return {'message': ['item 1', 'item 2']}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Validation Path params
@app.get("/items_validated/{request_id}")
async def read_item(request_id: Annotated[int, Path(ge=10, lt=15)]):
    return {"request_id": request_id}

# Enums as parameters values

class RequestTypes(str, Enum):
    service = 'service'
    new_feature = 'new_feature'

@app.get("/requests/type/{request_type}")
async def read_item(request_type: RequestTypes):
    return {"request_type": request_type.value}

# # * * * * * * * * * * * 
# Query parameters

@app.get('/test')
async def get_test(text: str):
    return {'test_request': text}

@app.get('/num_test')
async def get_num_test(num: int):
    return {'num': num}

@app.get("/query_params")
async def read_item(req: str, page: int = 10, skip: int = 0):
    return {
        "page": page,
        "skip": skip,
        "req": req
    }

# Validation query params
@app.get("/query_params_typed")
async def read_item(req: Annotated[str, Query(min_length=5, max_length=15)]):
    return {
        "req": req
    }

# Using default value
@app.get("/query_params_default")
async def read_item(req: Annotated[str, Query(min_length=5, max_length=15)]='default striing'):
    return {
        "req": req
    }

# Using regular expresion
@app.get("/query_params_regular")
async def read_item(req: Annotated[str, Query(min_length=5, max_length=15, pattern=r'test*')]='default striing'):
    return {
        "req": req
    }

# List params
#http://localhost:5002/items/?q=foo&q=bar
@app.get("/query_params_list")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items

# List params with defaults
@app.get("/query_params_list_default")
async def read_items(q: Annotated[list[str] | None, Query()] = ['foo', 'bar']):
    query_items = {"q": q}
    return query_items


# * * * * * * * * * * * 
# Body parameters

@app.post("/")
async def read_item(request: Request):
    return {
        "headers": request.headers,
        "cooke": request.cookies,
        "body": await request.body()
    }

# Form data
@app.put('/items')
async def put_items_data(username: Annotated[str, Form()],
                         password: Annotated[str, Form()]):
    return {
        'username': username,
        'password': password
    }

# Multiple body parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

# File mode upload
@app.put('/file')
async def put_file(file: Annotated[bytes, File()]):
    return {'file size': len(file)}

def main():
    uvicorn.run("Open_day_fastapi_pydantic:app", port=5002, reload=True, log_level='debug')

# # * * * * * * * * * * * * * * * 
# Dependencies

from fastapi import Depends, Cookie, Header, HTTPException

common_app = FastAPI()

# часто используемые параметры в отдельном методе

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@common_app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@common_app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


# Зависимости, сгруппированные в класс

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@common_app.get("/class_items")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

# Вложенные зависимости
def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@common_app.get("/cookie_items")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
):
    return {"q_or_cookie": query_or_default}


# Зависимости, использумеые для завершения работы метода, в случае если запрос не прошел валидацию
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@common_app.get("/validate_items", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

if __name__ == '__main__':
    main()
