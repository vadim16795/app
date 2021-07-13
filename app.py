from flask import Flask, render_template, jsonify
import psycopg2
import time
from data import Articles

app = Flask(__name__)

Articles_return = Articles()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/ping')
def ping():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


@app.route('/select')
def select():
    connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
                                  host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    cursor = connection.cursor()
    select_query = """ SELECT * FROM characters"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    if records is not None:
        return "OK"
    connection.close()
    cursor.close()


@app.route('/create')
def create_table():
    connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
                                  host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    cursor = connection.cursor()
    create_table_query = (
        "CREATE TABLE characters ( id SERIAL, name character varying, gender character varying,homeworld character varying);")
    cursor.execute(create_table_query)
    connection.commit()
    time.sleep(3)
    select_query = """ SELECT * FROM characters"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    if records is not None:
        return "Table created"
    connection.close()
    cursor.close()


@app.route('/test')
def articles():
    return render_template('articles.html', articles=Articles_return)
