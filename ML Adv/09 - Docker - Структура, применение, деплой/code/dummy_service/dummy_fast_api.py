from fastapi import FastAPI
from model import Model
from contextlib import asynccontextmanager


model = Model('FastAPI dummy model')

app = FastAPI()

# create a route
@app.get("/")
def index():
    return {"message": "FastAPI Hello World"}

@app.get("/predict")
def predict_sentiment(text=''):
    response = model.predict(text)
    return response
