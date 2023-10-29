import json
from model.util import group
from model.db import mongo


def record(done,score,rawdata,i_id):
    return {
        "Invite_detail":mongo.db.Invite_detail.update_many(
            {"i_id": i_id},
            [
                {'$set': {
                    'done': {
                        '$switch': {
                            'branches': done,
                            'default': []
                        }
                    },
                    'score': {
                        '$switch': {
                            'branches': score,
                            'default': 0
                        }
                    }
                }}
            ]
        ),
        "raw": mongo.db.record.insert_many(rawdata)
    }

        # "Invite_detail":mongo.db.Invite_detail.update_one(
        #     {
        #         'user_id': detail["user_id"],
        #         'i_id': detail["i_id"]
        #     },
        #     {
        #         '$set': {
        #             'done': detail["done"],
        #             'score': detail["score"]
        #         }
        #     }
        # ),



# def record(a_id,done,target):
#     return {
#         "appointment": mongo.db.appointment.update_one(
#             {"id": a_id}, {"$set": {"done": done}}
#         ),
#         "raw": mongo.db.rehabilion.insert_many(target),
#     }
