import json
from model.util import group
from model.db import mongo


def record(i_id,done,target):
    return {
        "appointment": mongo.db.appointment.update_one(
            {"id": i_id}, {"$set": {"done": done}}
        ),
        "raw": mongo.db.rehabilion.insert_many(target),
    }
