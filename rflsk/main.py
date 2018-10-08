from flask import Flask
from bluetest import bp
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.register_blueprint(bp)
    app.run(debug=True)