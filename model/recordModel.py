import json
from model.util import group
from model.db import mongo


def record(a_id,done,target):
    return {
        "appointment": mongo.db.appointment.update_one(
            {"id": a_id}, {"$set": {"done": done}}
        ),
        "raw": mongo.db.rehabilion.insert_many(target),
    }
