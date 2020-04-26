import os
import pymysql
from pymysql.cursors import DictCursor

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

DB = pymysql.connect(
    host=DB_HOST,
    port=int(DB_PORT),
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

COLUMNS = ['chat_id', 'store_id', 'store_hash', 'location', 'store_name']


def insert(chat_id, store_id, store_hash, location, store_name):

    select_columns = ','.join(COLUMNS)
    select_query = f'SELECT {select_columns} FROM store WHERE store_id = %s and store_hash = %s'
    insert_query = f'INSERT INTO store ({select_columns}) VALUES (%s, %s, %s, %s, %s)'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(select_query, [store_id, store_hash])
    store = cursor.fetchone()
    cursor.close()
    with DB.cursor(DictCursor) as cursor:
        insert_location = store['location'] if store and 'location' in store else location
        cursor.execute(insert_query, [chat_id, store_id, store_hash, insert_location, store_name])
        rowcount = cursor.rowcount
        print(rowcount)
    DB.commit()


def remove(chat_id, store_id):
    remove_query = f'DELETE FROM store WHERE chat_id = %s and store_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(remove_query, [chat_id, store_id])
    DB.commit()


def get_stores():
    query = """
        SELECT DISTINCT
            store_id, location, store_name
        FROM
            store;
    """
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(query)
        return cursor.fetchall()
