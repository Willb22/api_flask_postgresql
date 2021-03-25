from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, Response, jsonify
import json

from rules_triggers import *

'''
Below are functions called on different http methods received by the flask application.
These will write data passed in json format to the postresql tables modelled in models.py
Rules related to what data can or can not be insert to the tables are expressed in
funcitons check_character_valid and check_hat_valid
'''

db.init_app(app)

def check_character_valid(data):
    result = ""
    if 'age' in data.keys():
        if data['age'] >0:
            result = 'valid'
        else:
            result = 'age must be greater than zero'
    if 'human' in data.keys() and 'weight' in data.keys():
        if data['human']==True and data['weight'] >80:
            if 'age' not in data.keys():
                result = 'Please enter an age'
            else:
                if data['age']<10:
                    result = 'Please do not enter a heavy human under age 10'
                else:
                    result = 'valid'
        else:
            result = 'valid'
    else:
        result = 'valid'
    return result


def check_hat_valid(data_character, data_hat):
    result = "valid"
    if data_character:
        if 'human' in data_character.keys():
            if data_character['human']==False:
                result = 'Cannot add hat. Related human is False'

        if 'color' in data_hat.keys():
            if data_hat['color'] == 'yellow':
                if 'name' in data_character.keys():
                    if 'p' in data_character['name'].lower():
                        result = 'Please change color, or remove letter p from character name '
    else:
        result = 'A human must be provided for hat'
    return result



###### ######  Opérations CRUD sur tableau Character et Hat
###### ############ ######

@app.route('/apirestful/')
def view_database():
    print( 'inside view database', jsonify({"characters" : Character.view_all(), "hats" : Hat.view_all()}))
    return jsonify({"characters" : Character.view_all(), "hats" : Hat.view_all()})



@app.route('/apirestful/', methods=['POST'])
def add_character_id():
    request_data = request.get_json()  # getting data from client

    if 'characters' in request_data.keys() and 'hats' in request_data.keys() :
        data_characters = request_data['characters']
        print([key for key in data_characters.keys()])
        _check = check_character_valid(data_characters)
        if _check == 'valid':
            _name, _age, _weight, _human = [None] * 4
            if 'name' in data_characters.keys():
                _name = data_characters['name']
                print( ' name is ', _name)
            if 'age' in data_characters.keys():
                _age = data_characters['age']
                print(' age is ', _age)
            if 'weight' in data_characters.keys():
                _weight = data_characters['weight']
                print( 'w is ', _weight)
            if 'human' in data_characters.keys():
                _human = data_characters['human']
                print( ' human is ', _human)

            data_hats = request_data['hats']
            _check = check_hat_valid(data_characters, data_hats)
            if _check == 'valid':
                hat_foreingkey = Character.add_character(name=_name, age=_age, weight=_weight, human=_human)
                character_added = True
                _col = None
                if 'color' in data_hats.keys():
                    _col = data_hats['color']
                Hat.add_hat(color=_col, character_id=hat_foreingkey)

                request_data['hats'].update({'id' : hat_foreingkey})
                request_data['characters'].update({'id': hat_foreingkey})

                response = Response(json.dumps(request_data), 201, mimetype='application/json')
                print(json.dumps(request_data))

            else:
                response = _check
        else:
            response = _check
    else:
        response = "Please enter a key for characters and a key for hats"

    return response


@app.route('/apirestful/<int:id>', methods=['PUT'])
def update_character(id):

    request_data = request.get_json()  # getting data from client
    if 'characters' in request_data.keys() and 'hats' in request_data.keys():
        to_update_characters = request_data['characters']
        to_update_hats = request_data['hats']

        if Character.query.filter_by(id=id).count() > 0:
            row = Character.query.filter_by(id=id).first()
            if 'name' not in to_update_characters.keys() and row.name is not None:
                to_update_characters.update({'name' : row.name})
            if 'age' not in to_update_characters.keys() and row.age is not None:
                to_update_characters.update({'age' : row.age})
            if 'weight' not in to_update_characters.keys() and row.weight is not None:
                to_update_characters.update({'weight': row.weight})
            if 'human' not in to_update_characters.keys() and row.human is not None:
                to_update_characters.update({'human' : row.human})

            _check = check_character_valid(to_update_characters)
            if _check == 'valid':
                to_update_hats = request_data['hats']
                if Hat.query.filter_by(id = id).count()>0:
                    row = Hat.query.filter_by(id=id).first()
                    if 'color' not in to_update_hats.keys() and row.color is not None:
                        to_update_hats.update({'color':row.color})
                _check = check_hat_valid(to_update_characters, to_update_hats)
                if _check=='valid':
                    Character.query.filter_by(id=id).update(to_update_characters)
                    db.session.commit()

                    response = Response(json.dumps({"characters" : Character.view_character(_id=id), "hats" : Hat.view_hat(_id=id)}), 201, mimetype='application/json')

                    if 'color' in to_update_hats.keys():

                        Hat.query.filter_by(id=id).update(to_update_hats)
                        db.session.commit()
                        response = Response(json.dumps({"characters" : Character.view_character(_id=id), "hats" : Hat.view_hat(_id=id)}), 201, mimetype='application/json')


                else:
                    response = _check
            else:
                response = _check
        else:
            response = "Please provide an existing character id in URL"
    else:
        response = "Please enter a key for characters and a key for hats"

    return response



###### ######  Opérations CRUD sur tableau Character
###### ############ ######

@app.route('/apirestful/characters/')
def view_characters():
    return jsonify({"characters" : Character.view_all()})


@app.route('/apirestful/characters/<int:id>', methods=['GET'])
def view_character_id(id):
    if Character.query.filter_by(id=id).count() < 1:
        result = "Please provide an existing primary key"

    else:
        result = jsonify(Character.view_character(id))

    return result

@app.route('/apirestful/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    if Character.query.filter_by(id=id).count() > 0:

        Character.delete_character(id)
        response = Response(str("User " + str(id) + " Deleted"), 201, mimetype='application/json')
    else:
        response = "Please provide an existing primary key"

    return response

###### ######  Opérations CRUD sur tableau Hat
###### ############ ######


@app.route('/hats/')
def view_hats():
    return { "hats" : Hat.view_all()}

@app.route('/hats/<int:id>', methods=['GET'])
def view_hat_id(id):
    if Hat.query.filter_by(id=id).count() < 1:
        result = "Please provide an existing primary key"
    else:
        result = jsonify(Hat.view_hat(id))
    return result

@app.route('/hats/<int:id>', methods=['DELETE'])
def delete_hat(id):
    if Hat.query.filter_by(id=id).count() > 0:

        Hat.delete_hat(id)
        response = Response(str("Hat " + str(id) + " Deleted"), 201, mimetype='application/json')
    else:
        response = "Please provide an existing primary key"

    return response

if __name__ == '__main__':
    app.run(debug=True)
