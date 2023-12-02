import json
from model.util import group
from model.db import mongo
from datetime import datetime, timedelta


# 歷史運動列表
def getList(id, friend_id="", i_id=""):
    match = {
        "$match": {
            "user_id": id,
            "accept": 1,
        }
    }
    if i_id != None and i_id != "":
        match["$match"]["i_id"] = int(i_id)
    else:
        match["$match"]["$expr"] = {"$gt": [{"$size": "$done"}, 0]}
    
    pipline = [
        match,
        {
            "$lookup": {
                "from": "Invite",
                "localField": "i_id",
                "foreignField": "id",
                "as": "i_data",
            }
        },
        {"$unwind": "$i_data"},
        {
            "$addFields": {
                "name": "$i_data.name",
                "time": "$i_data.time",
                "m_id": "$i_data.m_id",
                "friend": "$i_data.friend",
                "avgScore": "$i_data.score",
                "remark": "$i_data.remark",
            }
        },
        {
            "$lookup": {
                "from": "user",
                "localField": "m_id",
                "foreignField": "id",
                "as": "m_data",
            }
        },
        {"$unwind": "$m_data"},
        {"$addFields": {"m_name": "$m_data.name"}},
        {"$unset": ["_id", "i_data", "m_data", "user_id", "accept"]},
        {"$sort": {"time": -1}},
    ]
    if friend_id != "":
        pipline.append({"$match": {"friend": {"$in": [friend_id]}}})
    return list(mongo.db.Invite_detail.aggregate(pipline))


def getHistory(h_id):
    
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {"$match": {"i_id": int(h_id), "accept": 1}},
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "user_id",
                        "foreignField": "id",
                        "as": "m_data",
                    },
                },
                {"$unwind": "$m_data"},
                {
                    "$addFields": {
                        "name": "$m_data.name",
                        "birthday": "$m_data.birthday",
                        "sex": "$m_data.sex",
                    }
                },
                {
                    "$lookup": {
                        "from": "Invite",
                        "localField": "i_id",
                        "foreignField": "id",
                        "as": "i_data",
                    },
                },
                {"$unwind": "$i_data"},
                # {"$addFields": {"name": "$i_data.m_id"}},
                {
                    "$unset": [
                        "_id",
                        "i_data",
                        "m_data",
                    ]
                },
            ]
            # {"i_id": int(h_id)}, {"_id": 0}
        )
    )


def getCommend(user_id, id=-1):
    pipline = {
        "$match": {
            "user_id": user_id,
            "$expr": {"$gt": [{"$size": "$done"}, 0]},
        }
    }
    if id != -1:
        pipline["$match"]["i_id"] = {"$lte": int(id)}
    
    data = list(
        mongo.db.Invite_detail.aggregate(
            [
                pipline,
                {"$sort": {"i_id": -1}},
                {"$unset": ["_id"]},
                {"$limit": 6},
            ]
        )
    )
    
    each_score = [0, 0, 0]
    baseline = data[0]["each_score"]
    for d in data[1::]:
        each = d["each_score"]
        if isinstance(each, list):
            for i in range(len(each)):
                each_score[i] += each[i]
    for i in range(len(each_score)):
        each_score[i] /= len(data) - 1
    each_commend = []
    for b, c in zip(baseline, each_score):
        commend = ""

        if b == c:
            commend = "繼續保持" if b >= 4 else "有待進步"
        elif b < c:
            commend = "稍有退步" if b == 4 else "有待進步"
        else:
            commend = "有進步"
        each_commend.append(commend)
    return each_commend
