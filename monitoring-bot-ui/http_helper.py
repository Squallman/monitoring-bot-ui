import requests
import json


def get(url):
    response = requests.get(url=url)
    result = response.json()
    return result


def post(url, data):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    result = response.json()
    return result
