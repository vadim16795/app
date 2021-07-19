from flask import Flask, render_template, jsonify
import psycopg2
import truncate_func
import urllib.request
import json
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/select')
def select():
    try:
        connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
                                      host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e)
        resp.status_code = 500
        return resp

    cursor = connection.cursor()
    select_query = """ SELECT * FROM characters"""
    try:
        cursor.execute(select_query)

    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e)
        resp.status_code = 500
        return resp

    data = cursor.fetchall()
    return render_template('characters.html', title='Characters', data=data)


def insert_func(api_url):
    try:
        connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
                                      host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e)
        resp.status_code = 500
        return resp
    cursor = connection.cursor()
    api_url_response = urllib.request.urlopen(api_url)
    api_url_response_page = api_url_response.read().decode('utf-8')
    parsed_page = json.loads(api_url_response_page)
    for i in range(0, len(parsed_page['results'])):
        homeworld_url = (parsed_page['results'][i]['homeworld'])
        api_url_response = urllib.request.urlopen(homeworld_url)
        api_url_response_page = api_url_response.read().decode('utf-8')
        parsed_page_homeworld = json.loads(api_url_response_page)
        insert_query = """ INSERT INTO characters (name, gender,homeworld) VALUES (%s,%s,%s)"""
        values_to_insert = (
            parsed_page['results'][i]['name'], parsed_page['results'][i]['gender'], parsed_page_homeworld['name'])
        try:
            cursor.execute(insert_query, values_to_insert)
            connection.commit()
        except psycopg2.Error as e:
            resp = jsonify(success=False, reason=e.pgerror)
            resp.status_code = 500
            return resp


@app.route('/updatedb')
def update_db():
    start_time = time.time()
    try:
        truncate_func.truncate_table("characters")
    except:
        resp = jsonify(success=False, error='failed to truncate table')
        resp.status_code = 500
        return resp
    url_list = []
    my_url = 'https://swapi.dev/api/people/'
    url_list.append(my_url)
    my_url_response = urllib.request.urlopen(my_url)
    my_url_response_page = my_url_response.read().decode('utf-8')
    parsed_page = json.loads(my_url_response_page)
    next_url = parsed_page['next']
    while next_url is not None:
        next_api_url = next_url
        api_url_response = urllib.request.urlopen(next_url)
        api_url_response_page = api_url_response.read().decode('utf-8')
        parsed_page = json.loads(api_url_response_page)
        next_url = parsed_page['next']
        url_list.append(str(next_api_url))
    for i in url_list:
        insert_func(i)
    end_time = time.time() - start_time
    resp = jsonify(success=True, time=str(end_time))
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run()
