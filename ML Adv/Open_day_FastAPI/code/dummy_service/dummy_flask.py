from flask import Flask, request
from model import Model


app = Flask(__name__)

model = Model('dummy_model')

@app.route('/')
@app.route('/index')
def index():
    return {'message': 'Hello FlaskAPI'}


@app.route('/fit')
def get_fit():
    data_string = request.args.get('data')
    response = model.fit(data_string)
    return {'message': response}

@app.route('/predict')
def get_predict():
    data_string = request.args.get('data')
    response = model.predict(data_string)
    return {'message': response} 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
