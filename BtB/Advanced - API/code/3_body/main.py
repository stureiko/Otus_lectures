from typing import Annotated

from fastapi import FastAPI, Form, File
from starlette.requests import Request

app = FastAPI()

# Request object


@app.post("/")
async def read_item(request: Request):
    return {
        "headers": request.headers,
        "cooke": request.cookies,
        "body": await request.body()
    }


@app.post("/form")
async def read_item(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {
        "username": username,
        "password": password
    }


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
