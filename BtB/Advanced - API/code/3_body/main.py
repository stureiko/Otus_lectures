from typing import Annotated

from fastapi import FastAPI, Form, File
from starlette.requests import Request

import uvicorn

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

def main():
    uvicorn.run(app=app, host='0.0.0.0', port=8002)
    
if __name__ == '__main__':
    main()