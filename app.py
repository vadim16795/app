from flask import Flask, render_template, jsonify
import psycopg2
import truncate_func
import urllib.request
import json
import time
import db
import docker_settings

app = Flask(__name__)
app.config.from_object('production_settings')
app.config.from_envvar('DOCKERAPP_CONFIG', silent=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/planets')
def planets():
    try:
        connection = psycopg2.connect(dbname=docker_settings.DBNAME, dbuser=docker_settings.USER, dbpassword=docker_settings.PASSWORD,
                                      host=docker_settings.HOST)
    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e.pgerror, message="cant connect to database")
        resp.status_code = 500
        return resp

    cursor = connection.cursor()
    select_query = """ SELECT * FROM planets"""
    try:
        cursor.execute(select_query)

    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e)
        resp.status_code = 500
        return resp

    data = cursor.fetchall()
    return render_template('planets.html', title='Planets', data=data)


@app.route('/characters')
def characters():
    try:
        connection = psycopg2.connect(dbname=db.dbname, user=db.user, password=db.password,
                                      host=db.host)
    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e.pgerror, message="cant connect to database")
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


def characters_insert_func(api_url):
    try:
        connection = psycopg2.connect(dbname=db.dbname, user=db.user, password=db.password,
                                      host=db.host)
    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e.pgerror, message='cant connect to database')
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


def planets_insert_func(api_url):
    try:
        connection = psycopg2.connect(dbname=db.dbname, user=db.user, password=db.password,
                                      host=db.host)
    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e.pgerror, message='cant connect to database')
        resp.status_code = 500
        return resp
    cursor = connection.cursor()
    api_url_response = urllib.request.urlopen(api_url)
    api_url_response_page = api_url_response.read().decode('utf-8')
    parsed_page = json.loads(api_url_response_page)
    for i in parsed_page['results']:

        if len(i['residents']) > 0:
            residents_list = []
            for element in i['residents']:
                api_url_response = urllib.request.urlopen(element)
                api_url_response_page = api_url_response.read().decode('utf-8')
                parsed_page_residents = json.loads(api_url_response_page)

                residents_list.append(parsed_page_residents['name'])

            #            print('Name=', i['name'], '|', 'Gravity=', i['gravity'], '|', 'Climate=', i['climate'], '|', 'Residents = ',
            #                  residents_list)
            insert_query = """ INSERT INTO planets (name, gravity,climate,residents) VALUES (%s,%s,%s,%s)"""
            values_to_insert = (
                str(i['name']), str(i['gravity']), str(i['climate']), residents_list)
            try:
                cursor.execute(insert_query, values_to_insert)
                connection.commit()
            except psycopg2.Error as e:
                resp = jsonify(success=False, reason=e.pgerror)
                resp.status_code = 500
                return resp
        else:
            #            print('Name=', i['name'], '|', 'Gravity=', i['gravity'], '|', 'Climate=', i['climate'], '|', 'Residents = ',
            #                  'None')
            insert_query = """ INSERT INTO planets (name, gravity,climate) VALUES (%s,%s,%s)"""
            values_to_insert = (
                str(i['name']), str(i['gravity']), str(i['climate']))

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
        truncate_func.truncate_table("planets")
    except psycopg2.Error as e:
        resp = jsonify(success=False, reason=e.pgerror, message='cant truncate one or more tables')
        resp.status_code = 500
        return resp
    people_url_list = []
    people_url = 'https://swapi.dev/api/people/'
    people_url_list.append(people_url)
    people_url_response = urllib.request.urlopen(people_url)
    people_url_response_page = people_url_response.read().decode('utf-8')
    parsed_page = json.loads(people_url_response_page)
    next_url = parsed_page['next']
    while next_url is not None:
        next_api_url = next_url
        api_url_response = urllib.request.urlopen(next_url)
        api_url_response_page = api_url_response.read().decode('utf-8')
        parsed_page = json.loads(api_url_response_page)
        next_url = parsed_page['next']
        people_url_list.append(str(next_api_url))
    for i in people_url_list:
        characters_insert_func(i)

    planets_url_list = []
    planets_url = 'https://swapi.dev/api/planets'
    planets_url_list.append(planets_url)
    planets_url_response = urllib.request.urlopen(planets_url)
    planets_url_response_page = planets_url_response.read().decode('utf-8')
    parsed_page = json.loads(planets_url_response_page)
    next_url = parsed_page['next']
    while next_url is not None:
        next_api_url = next_url
        api_url_response = urllib.request.urlopen(next_url)
        api_url_response_page = api_url_response.read().decode('utf-8')
        parsed_page = json.loads(api_url_response_page)
        next_url = parsed_page['next']
        planets_url_list.append(str(next_api_url))
    for i in planets_url_list:
        planets_insert_func(i)
    end_time = time.time() - start_time
    resp = jsonify(success=True, time=str(end_time))
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run()
