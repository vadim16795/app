import psycopg2
from flask import jsonify
import os



def truncate_table(tablename):
    connection = psycopg2.connect(dbname=os.getenv('DBNAME'), user=os.getenv('USER'), password=os.getenv('PASSWORD'),
                                  host=os.getenv('HOST'))
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE %s" % tablename)
    connection.commit()
    return
