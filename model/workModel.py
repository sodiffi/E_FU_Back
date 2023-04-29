import json
from model.util import group
from model.db import mongo
from datetime import datetime,timedelta


def getWork(t_id):
    return list(mongo.db.work.find({"t_id":t_id},{"_id":0}))

def addWork(t_id,start_date,work):
    start_date +="  00:00:00"
    datetime_object = datetime.strptime(f'{start_date}', '%Y-%m-%d %H:%M:%S')
    return mongo.db.work.insert_one({"t_id":t_id,"start_date":datetime_object,"work":work})