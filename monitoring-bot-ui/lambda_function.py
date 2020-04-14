import json
import os
import pymysql
import requests

TELEGRAM_SEND_URL = 'https://api.telegram.org/bot%(token)s/sendMessage?chat_id=%(chat_id)s' \
                    '&parse_mode=Markdown&text=%(message)s'

TELEGRAM_SEND_URL_v2 = 'https://api.telegram.org/bot%(token)s/sendMessage'

TOKEN = os.getenv('TOKEN')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', 3306)
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# DB = pymysql.connect(
#     host=DB_HOST,
#     port=3306,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     database=DB_NAME
# )




def lambda_handler(event, context):
    if 'message' in event:
        message = event.get('message')
        text = message.get('text') if 'text' in message else ''
        chat = message.get('chat') if 'chat' in message else ''
        chat_id = chat.get('id') if 'id' in chat else ''
        if '/start' in text.lower():
            t_message = 'This bot will help you to find available slots in Zakaz.ua try to put ' \
                        '"start" to start monitoring or "stop" to stop it.'
            telegram_send_message(TOKEN, chat_id, t_message)
        elif 'start' in text.lower():
            if exists(user_id=chat_id):
                t_message = 'Your id is already in the monitoring list.'
                telegram_send_message(TOKEN, chat_id, t_message)
            else:
                t_message = '👍Looking for available slots was started.'
                add_user(chat_id)
                telegram_send_message(TOKEN, chat_id, t_message)
        elif 'stop' in text.lower():
            if not exists(user_id=chat_id):
                t_message = 'Cannot find your id in the monitoring list'
                telegram_send_message(TOKEN, chat_id, t_message)
            else:
                t_message = '👎Looking for available slots was stopped.'
                remove_user(chat_id)
                telegram_send_message(TOKEN, chat_id, t_message)
        else:
            t_message = '🤦Bot doesn\'t support this command, try "start" or "stop".'
            telegram_send_message(TOKEN, chat_id, t_message)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def telegram_send_message(token, chat_id, message):
    params = {'token': token, 'chat_id': chat_id, 'message': message}
    url = TELEGRAM_SEND_URL % params
    requests.get(url=url)


def add_user(user_id):
    sql_query = 'INSERT INTO tbl_user (user_id) VALUES (%s);'
    with DB.cursor() as cursor:
        cursor.execute(sql_query, user_id)
    # DB.commit()


def remove_user(user_id):
    sql_query = 'DELETE FROM tbl_user WHERE user_id = %s;'
    with DB.cursor() as cursor:
        cursor.execute(sql_query, user_id)
    # DB.commit()


# def exists(user_id):
#     sql_query = 'SELECT user_id FROM tbl_user WHERE user_id = %s;'
#     with DB.cursor() as cursor:
#         cursor.execute(sql_query, user_id)
#         result = cursor.fetchone()
#         return True if result else False


import http_helper
# http_helper.get_auchan_dates()
http_helper.telegram_send_message(TOKEN)
# http_helper.convert_date('2020-04-07')
# http_helper.calculate_end_time(1586264400000.0)