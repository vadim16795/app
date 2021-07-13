from flask import Flask, render_template, jsonify
import psycopg2
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
    try:
        connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
                                      host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e)
        resp.status_code = 500
        return resp
    cursor = connection.cursor()

    create_table_query = (
        "CREATE TABLE characters ( id SERIAL, name character varying, gender character varying,homeworld character varying);")
    try:
        cursor.execute(create_table_query)
        connection.commit()
        connection.close()
        cursor.close()
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

    except psycopg2.Error as e:
        resp = jsonify(success=False,reason = e.pgerror)
        resp.status_code = 500
        return resp


@app.route('/test')
def articles():
    return render_template('articles.html', articles=Articles_return)

if __name__ == '__main__':
    app.run()