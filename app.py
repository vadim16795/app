from flask import Flask, render_template, jsonify
import psycopg2
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ping')
def ping():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

@app.route('/select')
def select():
    connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!', host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    cursor = connection.cursor()
    select_query = """ SELECT * FROM characters"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    if records is not None:
        return "OK"


