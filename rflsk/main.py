from flask import Flask
from bluetest import bp
from flask_mako import MakoTemplates
from flask_mako import render_template

app = Flask(__name__)
mako = MakoTemplates(app)

@app.route('/index')
def hello_world():
    # return 'Hello, World!'
    return render_template('index.html',{'aa':22})

if __name__ == '__main__':
    app.register_blueprint(bp)
    app.run(debug=True)