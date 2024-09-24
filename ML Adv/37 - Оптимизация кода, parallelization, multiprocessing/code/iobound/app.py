from fastapi import FastAPI, HTTPException, Path
from pydantic_settings import BaseSettings 
from typing import Annotated
import pandas as pd
import os

class Settings(BaseSettings):
    data_path: str = '../data/reviews.csv'

settings = Settings()
df = pd.read_csv(settings.data_path)
app = FastAPI()

@app.get('/')
def get_root():
    return {'message': 'Hello'}

@app.get('/total')
async def get_total():
    return {'total': df.shape[0]}

@app.get('/texts/{text_id}')
async def get_text(text_id: Annotated[int, Path(ge=0, lt=df.shape[0])]):
    return {'text': df.iloc[text_id]['review']}