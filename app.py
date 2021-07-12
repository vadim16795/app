from flask import Flask, render_template,jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp