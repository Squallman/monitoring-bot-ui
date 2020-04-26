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

COLUMNS = ['date', 'title', 'store_hash', 'is_open', 'price', 'store_id', 'store_name']


def insert(items):
    for item in items:
        print(item)

    insert_clause = ','.join(COLUMNS)
    values_clause = ','.join([f'%({item})s' for item in COLUMNS])
    insert_query = f'INSERT INTO store_status ({insert_clause}) VALUES ({values_clause})'
    with DB.cursor(DictCursor) as cursor:
        cursor.executemany(insert_query, items)
    DB.commit()


def remove(date, title, store_hash):
    remove_query = f'DELETE FROM store_status WHERE date = %s AND title = %s AND store_hash = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(remove_query, [date, title, store_hash])
    DB.commit()


def select():
    select_clause = ','.join(COLUMNS)
    query = f'''
        SELECT 
            {select_clause}
        FROM
            store_status;
    '''
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(query)
        return cursor.fetchall()