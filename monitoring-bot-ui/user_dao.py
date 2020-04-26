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

COLUMNS = ['chat_id', 'location', 'store_1', 'store_2', 'store_1_status', 'store_2_status',
           'first_name', 'last_name', 'location_confirm', 'store_1_name', 'store_2_name']


def add_user(chat_id, first_name, last_name):
    sql_query = 'INSERT INTO state (chat_id, first_name, last_name) VALUES (%s, %s, %s);'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, [chat_id, first_name, last_name])
    DB.commit()


def remove_user(chat_id):
    sql_query = 'DELETE FROM state WHERE chat_id = %s;'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, chat_id)
    DB.commit()


def get_user(chat_id):
    fields = ','.join(COLUMNS)
    sql_query = f'SELECT {fields} FROM state WHERE chat_id = %s;'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, chat_id)
        return cursor.fetchone()


def set_location(location, chat_id):
    sql_query = 'UPDATE state ' \
                'SET location= %s, ' \
                '  location_confirm= 0,' \
                '  store_1 = null, ' \
                '  store_2 = null, ' \
                '  store_1_name = null, ' \
                '  store_2_name = null, ' \
                '  store_1_status = 0, ' \
                '  store_2_status = 0, ' \
                '  location_confirm= 0 ' \
                'WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, [location, chat_id])
    DB.commit()


def set_confirm_location(chat_id, value=0):
    sql_query = 'UPDATE state SET location_confirm= %s WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, [value, chat_id])
    DB.commit()


def set_store_1(chat_id, store_id, store_name):
    sql_query = 'UPDATE state SET store_1 = %s, store_1_name = %s WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        print(store_name)
        cursor.execute(sql_query, [store_id, store_name, chat_id])
    DB.commit()


def set_store_2(chat_id, store_id, store_name):
    sql_query = 'UPDATE state SET store_2 = %s, store_2_name = %s WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, [store_id, store_name, chat_id])
    DB.commit()


def remove_store_1(chat_id):
    sql_query = 'UPDATE state ' \
                'SET store_1 = null, store_1_name = null, store_1_status = 0 ' \
                'WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, chat_id)
    DB.commit()


def remove_store_2(chat_id):
    sql_query = 'UPDATE state ' \
                'SET store_2 = null, store_2_name = null, store_2_status = 0 ' \
                'WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, chat_id)
    DB.commit()


def start_monitoring_1(chat_id):
    sql_query = 'UPDATE state SET store_1_status = 1 WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, chat_id)
    DB.commit()


def start_monitoring_2(chat_id):
    sql_query = 'UPDATE state SET store_2_status = 1 WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, chat_id)
    DB.commit()


def stop_monitoring_1(chat_id):
    sql_query = 'UPDATE state SET store_1_status = 0 WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, chat_id)
    DB.commit()


def stop_monitoring_2(chat_id):
    sql_query = 'UPDATE state SET store_2_status = 0 WHERE chat_id = %s'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(sql_query, chat_id)
    DB.commit()


def get_users():
    columns = ','.join(COLUMNS)
    select_query = f'SELECT {columns} FROM state WHERE store_1_status = 1 or store_2_status = 1'
    with DB.cursor(DictCursor) as cursor:
        cursor.execute(select_query)
        return cursor.fetchall()
