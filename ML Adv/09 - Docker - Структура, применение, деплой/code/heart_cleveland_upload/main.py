from fastapi import FastAPI
import uvicorn
from schemas import PatientAnalysis
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from fastapi.encoders import jsonable_encoder


app = FastAPI()


def train_model():
    df = pd.read_csv('heart_cleveland_upload.csv')
    X_train, X_test, y_train, y_test = train_test_split(df.drop('condition', axis=1),
                                                    df['condition'].values,
                                                    test_size=0.3,
                                                    random_state=1,
                                                    stratify=df['condition'].values)
    pipe = make_pipeline(StandardScaler(), LogisticRegression())
    pipe.fit(X_train, y_train)  
    # Pipeline(steps=[('standardscaler', StandardScaler()),
    #             ('logisticregression', LogisticRegression())])
    score = pipe.score(X_test, y_test) 
    return pipe, score



model, accuracy = train_model()



@app.post("/predict/")
async def make_prediction(analysis:PatientAnalysis):
    # res = model.predict(transform_to_df(analysis))
    data = pd.DataFrame(jsonable_encoder(analysis), index=[0])
    print(data)
    res = model.predict(data)
    print(f'predict: {res}')
    return str(res[0])


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)