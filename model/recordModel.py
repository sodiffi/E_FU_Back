import json
from model.util import group
from model.db import mongo
from decimal import Decimal, ROUND_HALF_UP

def record(done,each_score,total_score,rawdata,i_id,user_id):
    mongo.db.Invite_detail.update_many(
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
        )
    mongo.db.record.insert_many(rawdata)
    sportsList = list(mongo.db.Invite_detail.find({"user_id": user_id}))
    score = [0, 0, 0]
    count = [0, 0, 0]
    for i in sportsList:
        for d in i["done"]:
            score[d["type_id"]] = score[d["type_id"]] + int(d["level"])
            count[d["type_id"]] = count[d["type_id"]] + 1
    for i in range(0, len(score)):
        if count[i] != 0:
            score[i] = score[i] / count[i]
    avg = Decimal(sum(score) / len(score))
    avg = float(avg.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
    return {
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
            score[d["type_id"]] = score[d["type_id"]] + int(d["level"])
            count[d["type_id"]] = count[d["type_id"]] + 1
    for i in range(0, len(score)):
        if count[i] != 0:
            score[i] = score[i] / count[i]
    avg = Decimal(sum(score) / len(score))
    avg = float(avg.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
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