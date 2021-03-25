
from models import *

from sqlalchemy import event
import time
from flask import jsonify

'''
Deleting an entry in table Character will trigger the associated entry in table Hat to also be deleted
'''




@db.event.listens_for(Character, "after_delete")
def delete_on_hat(mapper, connection, target):
    po = Hat.__table__
    tst = "delete from public.\""+str(po)+ "\" where id="+str(target.id)+";"
    connection.execute(tst)

@db.event.listens_for(Character, "after_delete")
def delete_on_hat(mapper, connection, target):
    po = Hat.__table__
    tst = "delete from public.\""+str(po)+ "\" where id="+str(target.id)+";"
    connection.execute(tst)


db.drop_all(bind=None) #delete table to reset from previous run


db.create_all()

db.session.commit()


