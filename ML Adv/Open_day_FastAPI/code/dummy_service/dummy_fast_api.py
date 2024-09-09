from fastapi import FastAPI
from model import Model


model = Model('FastAPI dummy model')

app = FastAPI()

# create a route
@app.get("/")
def index():
    return {"message": "FastAPI Hello World"}

@app.get('/fit')
def get_fit(data: str):
    response = model.fit(data)
    return {'messag': response}

@app.get("/predict")
def predict_sentiment(data: str):
    response = model.predict(data)
    return {'message': response}
