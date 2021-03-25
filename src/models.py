from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DDL, event
import enum
import json
import os
'''
Below are models defining postgresl tables to be created
'''

db_name ='python_flask_api'
user_connection = 'postgres'
password = os.environ.get('PASSPOSTGRES')

connection_postgresql_db = f"postgresql://{user_connection}:{password}@127.0.0.1/{db_name}"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_postgresql_db

db = SQLAlchemy(app)

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float,  nullable=True)
    human = db.Column(db.Boolean)
    hat_ = db.relationship('Hat', backref='character', uselist=False) # one to one relationship

    def json(self):
        return {'id': self.id, 'name': self.name,
                'age': self.age, 'weight': self.weight, 'human': self.human}

    def view_character(_id ):
        return [Character.json(Character.query.filter_by(id=_id).first())]

    def view_all():
        return [Character.json(el) for el in Character.query.all()]

    def add_character(id=None, name=None, age=None, weight=None, human=None):
        guest = Character(id=id, name=name, age=age, weight=weight, human=human)
        app.logger.info(guest.id)  # currently None, before persistence
        db.session.add(guest)
        db.session.commit()
        app.logger.info(guest.id)  # gets assigned an id of 1 after being persisted
        return guest.id

    def delete_character(id=None):
        dell = Character.query.filter_by(id=id).first()
        db.session.delete(dell)
        db.session.commit()


    def __repr__(self):
        return '<Character %r>' % self.id


class Color(str, enum.Enum):
    purple= "purple"
    yellow = "yellow"
    green = "green"



class Hat (db.Model):
    __tablename__ = 'hat'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Enum(Color))
    character_id = db.Column(db.Integer(), db.ForeignKey('character.id'))

    def json(self):
        return {'id': self.id, 'color': json.dumps(self.color).strip('"'),
                'character_id': self.character_id}


    def view_hat(_id):
        return [Hat.json(Hat.query.filter_by(id=_id).first())]

    def view_all():
        return [Hat.json(el) for el in Hat.query.all()]

    def add_hat(id=None, color=None, character_id = None):
        guest = Hat(id=id, color=color, character_id = character_id)
        app.logger.info(guest.id)
        db.session.add(guest)
        db.session.commit()
        app.logger.info(guest.id)  # gets assigned an id of 1 after being persisted

    def delete_hat(id=None):
        dell = Hat.query.filter_by(id=id).first()
        db.session.delete(dell)
        db.session.commit()

    def __repr__(self):
        return '<Hat %r>' % self.id

