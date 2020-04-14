import json

import requests
from datetime import date
import calendar
from datetime import datetime


TELEGRAM_SEND_URL = 'https://api.telegram.org/bot%(token)s/sendMessage'
TELEGRAM_GET_UPDATES_URL = 'https://api.telegram.org/bot%(token)s/getUpdates'
DELIVERY_SCHEDULE_URL = 'https://stores-api.zakaz.ua/stores/%s/delivery_schedule/plan/?coords=49.8647098,24.0292797'



STORES = [{
    'id': '48215637',
    'name': 'METRO Львів'
},{
    'id': '48246409',
    'name': 'Auchan Львів'    
}]


def get_auchan_dates():
    slots = []
    for store in STORES:
        store_id = store.get('id')
        store_slots = get_store_slots(store_id)
        slots.extend(store_slots)
    slots_by_date = [{slot.pop('date'): slot} for slot in slots]
    date_set = set()
    for slot in slots_by_date:
        keys = slot.keys()
        date_set = date_set.union(keys)
    result = []
    for day in sorted(date_set):
        converted_date = convert_date(day),
        result.append(converted_date[0])
        for item in slots_by_date:
            slot = item.get(day)
            if slot:
                title = slot.get('title'),
                status = f'✅' if slot.get('is_open') else f'❌',
                price = float(slot.get('price')) / 100,
                store_name = find_store_name(slot.get('store_id'))
                message = f'{status[0]} {title[0]} / {store_name} / {price[0]} uah'
                result.append(message)

    print(result)
    return '\n'.join(result)


example = {'id': '9bd92756f4b1f8d06e61e52367d799cd|lviv_shevchenkivskii-a', 'end_ordering_time': 1586264400000.0,
           'time_range': '20:00 - 22:00', 'price': 5900, 'currency': 'uah', 'is_open': True, 'date': '2020-04-07'}


def get_store_slots(store_id):
    url = DELIVERY_SCHEDULE_URL % store_id
    response = requests.get(url=url)
    if response.status_code == 200:
        result = []
        for day in response.json():
            for item in day.get('items'):
                slot = {
                    'date': item.get('date'),
                    'title': item.get('time_range'),
                    'is_open': item.get('is_open'),
                    'price': item.get('price'),
                    'store_id': store_id
                }
                result.append(slot)
        return result
    else:
        return []


def telegram_send_message(token):
    print(f'token={token}')
    params = {'token': token}
    url = TELEGRAM_SEND_URL % params
    print(url)
    text = get_auchan_dates()
    data = {
        'chat_id': TELEGRAM_ID,
        'text': text,
        'parse_mode': 'Markdown',
        'reply_markup': {
            'keyboard': [
                [{'text': 'start'}, {'text': 'stop'}],
                [{'text': 'back'}]
            ],
            'resize_keyboard': True,
            'one_time_keyboard': True
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    print(response.content)


def convert_date(input_date):
    n_date = date.fromisoformat(input_date)
    difference = n_date - datetime.now().date()
    return 'Today' if difference.days == 0 else 'Tomorrow' \
        if difference.days == 1 else f'{n_date.day} {calendar.month_name[n_date.month]}'

def find_store_name(store_id):
    for store in STORES:
        if store_id == store.get('id'):
            return store.get('name')
    return ''