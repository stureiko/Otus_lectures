from fastapi import FastAPI
from model import Model
import uvicorn


model = Model('FastAPI dummy model')

app = FastAPI()

# create a route
@app.get("/")
def index():
    return {"message": "FastAPI Hello World"}

@app.put('/fit')
def get_fit(data: str):
    response = model.fit(data)
    return {'messag': response}

@app.get("/predict")
def predict_get(data: str):
    response = model.predict(data)
    return {'message': response}

@app.put("/predict")
def predict_put(d: str):
    response = model.put_pred(d)
    return {'put_message': response}

def main():
    uvicorn.run(app=app, port=8080)

if __name__ == '__main__':
    main()
