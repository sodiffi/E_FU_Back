import json
from model.util import group
from model.db import mongo


def record(detail,rawdata):
    return {
        "Invite_detail":mongo.db.Invite_detail.update_one(
            {
                'user_id': detail["user_id"],
                'i_id': detail["i_id"]
            },
            {
                '$set': {
                    'done': detail["done"],
                    'score': detail["score"]
                }
            }
        ),
        "raw": mongo.db.record.insert_many(rawdata)
    }

# def record(a_id,done,target):
#     return {
#         "appointment": mongo.db.appointment.update_one(
#             {"id": a_id}, {"$set": {"done": done}}
#         ),
#         "raw": mongo.db.rehabilion.insert_many(target),
#     }
