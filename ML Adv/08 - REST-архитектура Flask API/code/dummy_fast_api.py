from fastapi import FastAPI
from contextlib import asynccontextmanager

app = FastAPI()

# create a route
@app.get("/")
def index():
    return {"message": "FastAPI Hello World"}

@app.get("/predict")
def predict_sentiment(text: str):
    response = {'predict': text}
    return response
