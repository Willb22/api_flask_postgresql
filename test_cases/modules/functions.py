

import requests
import json


def try_get(url, expected_return):

    re = requests.get(url)
    assert re.status_code == 200

    re_body = re.json()

    assert re_body == expected_return

def try_post(url,headers, payload, expected_return):
    headers = {'Content-Type': 'application/json'}
    re = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    assert re.status_code == 201

    re_body = re.json()

    assert re_body == expected_return

def try_delete(url, expected_return):
    re = requests.delete(url)
    assert re.status_code == 200

    re_body = re.json()

    assert re_body == expected_return

def try_put(url,headers, payload, expected_return):
    headers = {'Content-Type': 'application/json'}
    re = requests.put(url, headers=headers, data=json.dumps(payload, indent=4))

    assert re.status_code == 201

    re_body = re.json()

    assert re_body == expected_return