import json
from model.util import group
from model.db import mongo

def record(target):
    to_save=[]
    raw=json.loads(target['raw'])
    for b in raw:
        b['arrange_id']=target['arrange_id']
        to_save.append(b)
    return mongo.db.record.insert_many(to_save)
