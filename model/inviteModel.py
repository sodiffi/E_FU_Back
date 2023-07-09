import json
from model.util import group
from model.db import mongo
from datetime import datetime,timedelta

def addinviteid(data):
    #return mongo.db.inviteid.insert_one(data)
    try:
        mongo.db.inviteid.insert_one(data)
        return ""
    except:
        return "error"

""" def get():
    return mongo.db.user.insert_one(inviteid) """