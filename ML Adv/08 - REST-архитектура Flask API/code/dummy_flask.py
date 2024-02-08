from flask import Flask, request


app = Flask(__name__)

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

@app.route('/test')
def hello():
    return '''
<html>
    <head>
        <title>Flask API Test page</title>
    </head>
    <body>
        <div>Hello, this is test page for Flask API!</div>
    </body>
</html>'''

@app.route('/user/<name>')
def hello_user(name):
    return f'''
<html>
    <head>
        <title>Flask API Hello page</title>
    </head>
    <body>
        <h1>Hello, this is test page for user "{name}"</h1>
    </body>
</html>'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)