import psycopg2
from flask import jsonify
import os



def truncate_table(tablename):
    connection = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                                  host=os.getenv('DB_HOST'))
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE %s" % tablename)
    connection.commit()
    return

