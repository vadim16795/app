import psycopg2
from flask import jsonify
import db


def truncate_table(tablename):
    connection = psycopg2.connect(dbname=db.dbname, user=db.user, password=db.password,
                                  host=db.host)
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE %s" % tablename)
    connection.commit()
    return
