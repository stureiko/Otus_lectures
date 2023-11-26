from flask import Flask, request
from model import Model


app = Flask(__name__)

model = Model('dummy_model')

@app.route('/')
@app.route('/index')
def index():
    return '''
<html>
    <head>
        <title>Home Page - Flask API</title>
    </head>
    <body>
        <h1>Hello, this is dummy Flask API!</h1>
    </body>
</html>'''

# @app.route('/guess', methods=['POST'])
# def get_data():
#     if request.method == 'POST':
#         data_string = request.get_json()
#         response = model.predict(data_string)
#     return response

@app.route('/guess')
def get_data():
    data_string = request.args.get('text')
    response = model.predict(data_string)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)