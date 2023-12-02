import json
from model.util import group
from model.db import mongo


def record(done,each_score,total_score,rawdata,i_id,user_id):
    sportsList = list(mongo.db.Invite_detail.find({"user_id": user_id}))
    score = [0, 0, 0]
    count = [0, 0, 0]
    for i in sportsList:
        for d in i["done"]:
            # print(d)
            # print(type(d))
            score[d["type_id"]] = score[d["type_id"]] + int(d["level"])
            count[d["type_id"]] = count[d["type_id"]] + 1
    for i in range(0, len(score)):
        if count[i] != 0:
            score[i] = score[i] / count[i]
    avg = sum(score) / len(score)
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
                    'each_score': {
                        '$switch': {
                            'branches': each_score,
                            'default': 0
                        }
                    },
                    'total_score': {
                        '$switch': {
                            'branches': total_score,
                            'default': 0
                        }
                    }
                }}
            ]
        ),
        "raw": mongo.db.record.insert_many(rawdata),
        "score": mongo.db.user.update_one(
            {"id": user_id},
            {
                "$set": {
                    "sport_info.$[element1].score": score[0],
                    "sport_info.$[element2].score": score[1],
                    "sport_info.$[element3].score": score[2],
                    "score":avg
                }
            },
            array_filters=[
                {"element1.type_id": 0},
                {"element2.type_id": 1},
                {"element3.type_id": 2}
            ]
        )
    }

def avg_score(user_id):
    ##更新三項平均
    sportsList = list(mongo.db.Invite_detail.find({"user_id": user_id}))
    score = [0, 0, 0]
    count = [0, 0, 0]
    for i in sportsList:
        for d in i["done"]:
            # print(d)
            # print(type(d))
            score[d["type_id"]] = score[d["type_id"]] + int(d["level"])
            count[d["type_id"]] = count[d["type_id"]] + 1
    for i in range(0, len(score)):
        if count[i] != 0:
            score[i] = score[i] / count[i]
    avg = sum(score) / len(score)
    return mongo.db.user.update_one(
        {"id": user_id},
        {
            "$set": {
                "sport_info.$[element1].score": score[0],
                "sport_info.$[element2].score": score[1],
                "sport_info.$[element3].score": score[2],
                "score":avg
            }
        },
        array_filters=[
            {"element1.type_id": 0},
            {"element2.type_id": 1},
            {"element3.type_id": 2}
        ]
    )


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
