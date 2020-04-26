import store_status_dao


def process_slots(latest_list):
    previous_list = store_status_dao.select()
    new_items = compare_list(latest_list, previous_list)
    remove_items = compare_list(previous_list, latest_list)

    print(f'latest_list={len(latest_list)}')
    print(f'previous_list={len(previous_list)}')
    print(f'new_items={len(new_items)}')
    print(f'remove_items={len(remove_items)}')

    for item in remove_items:
        store_status_dao.remove(item['date'], item['title'], item['store_hash'])
        item['is_open'] = False
    store_status_dao.insert(new_items)
    return [*new_items, *remove_items]


def compare_list(list_1, list_2):
    result = []
    for new in list_1:
        is_present = False
        for old in list_2:
            if new['date'] == old['date'] \
                    and new['title'] == old['title'] \
                    and new['store_hash'] == old['store_hash']:
                is_present = True
        if not is_present:
            result.append(new)
    return result
