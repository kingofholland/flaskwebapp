from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Azure App Service!'

if __name__ == '__main__':
    # Running on http://127.0.0.1:5000 by default
    app.run()
