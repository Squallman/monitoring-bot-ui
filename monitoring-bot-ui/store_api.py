import calendar
import locale
import os
from datetime import datetime, date

import http_helper
import store_dao

locale.setlocale(locale.LC_ALL, 'uk_UA')

API_URL = os.getenv('API_URL')
DELIVERY_SCHEDULE_URL = API_URL + 'stores/{}/delivery_schedule/plan/?coords={}'


def remove_user_store(chat_id, store_id):
    store_dao.remove(chat_id, store_id)


def add_user_store(chat_id, store_id, store_name, location):
    slots = __get_store_slots(store_id, store_name, location)
    if slots and slots[0] and slots[0].get('store_hash'):
        store_hash = slots[0].get('store_hash')
        store_dao.insert(chat_id, store_id, store_hash, location, store_name)
        return build_store_result_message(slots)
    return ''


def build_store_result_message(slots):
    slots_by_date = [{slot.copy().pop('date'): slot} for slot in slots if slot.get('is_open')]
    date_set = set()
    for slot in slots_by_date:
        keys = slot.keys()
        date_set = date_set.union(keys)
    result = []
    for day in sorted(date_set):
        converted_date = __convert_date(day),
        result.append(converted_date[0])
        for item in slots_by_date:
            slot = item.get(day)
            if slot:
                store_name = slot.get('store_name')
                title = slot.get('title'),
                status = f'✅' if slot.get('is_open') else f'❌',
                price = float(slot.get('price')) / 100,
                message = f'{status[0]} {title[0]} / {store_name}'
                result.append(message)
    return '\n'.join(result)


def __get_store_slots(store_id, store_name, location):
    url = DELIVERY_SCHEDULE_URL.format(store_id, location)
    response = http_helper.get(url)
    return [{
        'date': item.get('date'),
        'title': item.get('time_range'),
        'is_open': item.get('is_open'),
        'price': item.get('price'),
        'store_id': store_id,
        'store_hash': item.get('id'),
        'store_name': store_name
    } for day in response for item in day.get('items') if item.get('is_open')]


def __convert_date(input_date):
    n_date = date.fromisoformat(input_date)
    difference = n_date - datetime.now().date()
    return '→ Today ←' if difference.days == 0 else '→ Tomorrow ←' \
        if difference.days == 1 else f'→ {n_date.day} {calendar.month_name[n_date.month]} ←'


def get_stores(coords='49.8647098,24.0292797'):
    url = f'{API_URL}stores/?coords={coords}'
    result = http_helper.get(url)
    return result
