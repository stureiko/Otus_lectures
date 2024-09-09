from flask import Flask, request


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return {'message': 'Hello Flask'}

@app.route('/test')
def hello():
    return {'message': 'Test message'}

@app.route('/user/<name>')
def hello_user(name):
    return {'message': f'User {name}'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
