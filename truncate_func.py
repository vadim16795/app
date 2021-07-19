import psycopg2
from flask import jsonify


def truncate_table(tablename):
    connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
                                  host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE %s" % tablename)
    connection.commit()
    return
