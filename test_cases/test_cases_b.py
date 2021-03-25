import requests
import json
from flask import jsonify
import modules

'''
1. Check all tables are initially empty
2. Perform POST request (Create)
3. Perform GET request (Read)
4. Perform PUT request (Update)

'''
url_root = 'http://127.0.0.1:5000/apirestful/'
more = 'characters/'
url = url_root + more
headers = {'Content-Type': 'application/json'}

def test_case_part_a():


    expected = {"characters" : [], "hats" : []}
    modules.try_get(url_root,expected )

def test_case_part_b():
    '''
    Test POST method
    :return:
    '''

    payload = {"characters": {"name": 'Maurine', "age": 5}, "hats": {'color' : 'purple'}}
    expected = {"characters": {"name": "Maurine", "age": 5, "id": 1}, "hats": {"color": "purple", "id": 1}}

    modules.try_post(url_root, headers=headers, payload=payload, expected_return=expected)

def test_case_part_c():
    '''
    test GET method on previously added entries in Character and Hat
    :return:
    '''
    expected = {"characters": [{"age": 5, "human": None, "id": 1, "name": "Maurine", "weight": None}], "hats": [{"character_id": 1, "color": "purple", "id": 1}]}

    modules.try_get(url_root, expected_return=expected)

def test_case_part_d():
    '''
    test PUT method on previously added entries in Character and Hat
    primary key attributed to each should be 1 in this test case
    the put method developped in app.py returns the full database query for the entry whose primary key is specified in
    the URL
    Eg: http://127.0.0.1:5000/apirestful/1 , method = [PUT]
    this will update entry whose primary key is 1


    :return:
    '''

    url = url_root+ str(1)
    print(url)
    payload = {"characters": {"name": 'Eloise'}, "hats": {}}
    expected = {"characters": [{"id": 1, "name": "Eloise", "age": 5, "weight": None, "human": None}], "hats": [{"id": 1, "color": "purple", "character_id": 1}]}

    modules.try_put(url,headers = headers,payload=payload, expected_return=expected)

def test_case_part_d():
    '''
    Test DELETE method on character table
    the DELETE method developped in app.py returns 'User 1 Deleted' if the database holds an entry of primary key 1
    Status code is set to 201 on success


    :return:
    '''


    url = url_root+ more+ str(1)
    print(url)

    expected_return = "User 1 Deleted"
    #modules.try_delete(url,headers = headers, expected_return=expected_return)

    re = requests.delete(url)
    assert re.status_code == 201

    re_body = re.text

    assert re_body == expected_return
