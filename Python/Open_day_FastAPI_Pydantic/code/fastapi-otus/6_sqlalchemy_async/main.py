import json
from typing import Annotated, Any

from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from orm import crud, models
from orm.database import SessionLocal, engine, Base

app = FastAPI()

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# Dependency
async def get_db() -> SessionLocal:
    async with SessionLocal() as session:
        yield session


@app.post("/users/")
async def create_user(request: Request, db: SessionLocal = Depends(get_db)):
    user = json.loads((await request.body()).decode('utf-8'))
    db_user = await crud.Users.get_by_email(db, email=user['email'])
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.Users.create(db=db, email=user['email'], password=user['password'])


@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await crud.Users.all(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud.Users.get(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/",)
async def create_item_for_user(
    request: Request, user_id: int, db: Session = Depends(get_db)
):
    item = json.loads((await request.body()).decode('utf-8'))
    return await crud.Users.Items.create(db=db, item_title=item['title'], item_description=item['description'], user_id=user_id)


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = await crud.Users.Items.all(db, skip=skip, limit=limit)
    return items