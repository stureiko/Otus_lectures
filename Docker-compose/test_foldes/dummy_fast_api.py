from fastapi import FastAPI
from model import Model


model = Model('FastAPI dummy model')

app = FastAPI()

# create a route
@app.get("/")
def index():
    return {"message": "FastAPI Hello World"}

@app.post('/fit')
def fit(example: str):
    response = model.fit(example=example)
    return response

@app.get("/predict")
def predict_sentiment():
    response = model.predict()
    return response
