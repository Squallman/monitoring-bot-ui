import user_dao
import telegram_api
import messages
import store_api
import bad_words
import commands


def default_handler(data):
    user = user_dao.get_user(data.get('chat_id'))
    if user:
        if data.get('location'):
            handle_location(data.get('location'), data.get('chat_id'))
        elif not user.get('location'):
            telegram_api.choose_location(user.get('chat_id'), messages.choice_location)
        elif data.get('text'):
            handle_message(data.get('text'), user)
        else:
            raise AttributeError('Not implemented attribute')
    else:
        handle_new_user(data.get('chat_id'), data.get('first_name'), data.get('last_name'))


def handle_message(input_message, user):
    chat_id = user.get('chat_id')
    store_1 = user.get('store_1_name')
    store_2 = user.get('store_2_name')
    if commands.change_location in input_message:
        user_dao.set_confirm_location(chat_id, 1)
        telegram_api.change_location_confirm(chat_id, messages.location_confirm)
    elif commands.yes in input_message and user.get('location_confirm') == 1:
        telegram_api.choose_location(chat_id, messages.choice_location)
    elif commands.no in input_message:
        default_message(chat_id, messages.make_your_choice)
    elif commands.change_store in input_message:
        store_list = store_api.get_stores(user.get('location'))
        stores = [store.get('name') for store in store_list]
        if store_1 in input_message:
            user_dao.remove_store_1(chat_id)
            if store_2 and store_2 in stores:
                stores.remove(store_2)
            telegram_api.new_stores(chat_id, messages.choose_store, stores)
        elif store_2 in input_message:
            user_dao.remove_store_2(chat_id)
            if store_1 and store_1 in stores:
                stores.remove(store_1)
            telegram_api.new_stores(chat_id, messages.choose_store, stores)
        else:
            default_message(chat_id, messages.error_change_store)
    elif commands.start_monitoring in input_message:
        if store_1 and store_1 in input_message:
            user_dao.start_monitoring_1(chat_id)
            default_message(chat_id, messages.started.format(store_1))
            store_api.add_user_store(
                chat_id, user.get('store_1'), user.get('store_1_name'), user.get('location'))
        elif store_2 and store_2 in input_message:
            user_dao.start_monitoring_2(chat_id)
            default_message(chat_id, messages.started.format(store_2))
            store_api.add_user_store(
                chat_id, user.get('store_2'), user.get('store_2_name'), user.get('location'))
        else:
            default_message(chat_id, messages.error_start_monitoring)
    elif commands.stop_monitoring in input_message:
        if store_1 in input_message:
            user_dao.stop_monitoring_1(chat_id)
            store_api.remove_user_store(chat_id, user.get('store_1'))
            default_message(chat_id, messages.stopped.format(store_1))
        elif store_2 in input_message:
            user_dao.stop_monitoring_2(chat_id)
            store_api.remove_user_store(chat_id, user.get('store_2'))
            default_message(chat_id, messages.stopped.format(store_2))
        else:
            default_message(chat_id, messages.error_start_monitoring)
    elif commands.add_new in input_message:
        if not store_2:
            store_list = store_api.get_stores(user.get('location'))
            stores = [store.get('name') for store in store_list]
            if store_1 and store_1 in stores:
                stores.remove(store_1)
            if stores:
                telegram_api.new_stores(chat_id, messages.choose_store, stores)
            else:
                default_message(chat_id, messages.no_more_store)

        else:
            default_message(chat_id, messages.error_command)
    elif store_1 and store_1 in input_message:
        telegram_api.present_stores_menu(chat_id, user.get('store_1_status'), store_1)
    elif store_2 and store_2 in input_message:
        telegram_api.present_stores_menu(chat_id, user.get('store_2_status'), store_2)
    else:
        store_list = store_api.get_stores(user.get('location'))
        print(store_list)
        stores = {store.get('name'): store.get('id') for store in store_list}
        if input_message in stores.keys():
            if not store_1:
                user_dao.set_store_1(chat_id, stores.get(input_message), input_message)
                telegram_api.present_stores_menu(chat_id, False, input_message)
            elif not store_2:
                user_dao.set_store_2(chat_id, stores.get(input_message), input_message)
                telegram_api.present_stores_menu(chat_id, False, input_message)
        elif bad_words.check_bad_words(input_message):
            default_message(chat_id, messages.error_bad_word)
        else:
            default_message(chat_id, messages.error_command)


def handle_location(location, chat_id):
    latitude = location.get('latitude')
    longitude = location.get('longitude')
    input_location = f'{latitude},{longitude}'
    user_dao.set_location(input_location, chat_id)
    store_list = store_api.get_stores(input_location)
    stores = [store.get('name') for store in store_list if store.get('name')]
    telegram_api.new_stores(chat_id, messages.choose_store, stores)


def default_message(chat_id, text):
    user = user_dao.get_user(chat_id)
    chat_id = user.get('chat_id')
    store_1_status = '✅' if user.get('store_1_status') == 1 \
        else '❌' if user.get('store_1_status') is not None else ''
    store_2_status = '✅' if user.get('store_2_status') == 1 \
        else '❌' if user.get('store_2_status') is not None else ''
    store_1_name = user.get('store_1_name')
    store_2_name = user.get('store_2_name')
    return telegram_api.default(store_1_status, store_1_name,
                                store_2_status, store_2_name, chat_id, text)


def handle_new_user(chat_id, first_name, last_name):
    user_dao.add_user(chat_id, first_name, last_name)
    telegram_api.choose_location(chat_id, messages.choice_location)


def convert(event):
    input_message = event.get('message')
    if input_message:
        text = input_message.get('text')
        location = input_message.get('location')
        chat = input_message.get('chat')
        if chat:
            chat_id = chat.get('id')
            return {
                'chat_id': chat_id,
                'location': location,
                'text': text,
                'first_name': chat.get('first_name'),
                'last_name': chat.get('last_name')
            }
    raise AttributeError('Not implemented attribute')
