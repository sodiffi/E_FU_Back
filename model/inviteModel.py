import json
from model.util import group, timeFormat, timeformatString
from model.db import mongo
from datetime import datetime, timedelta
import bson


def checkInvite(start):
    return list(
        mongo.db.Invite.find(
            {
                "$or": [
                    {"time": {"$lt": datetime.fromisoformat(start)}},
                    {
                        "time": {
                            "$gt": datetime.fromisoformat(start) + timedelta(hours=2)
                        }
                    },
                ]
            }
        )
    )


def addinvite(id, name, m_id, friend, time, remark):  # 新增邀約
    if (len(checkInvite(time))) <= 0:
        return mongo.db.Invite.insert_one(
            {
                "id": id,
                "name": name,
                "m_id": m_id,
                "friend": friend,
                "time": timeFormat(time),
                "remark": remark,
            }
        )
    else:
        return "無法新增"


def addinvitedetail(data):
    return mongo.db.Invite_detail.insert_many(data)


def editinvite(id, name, m_id, friend, time, remark):  # 修改邀約
    if (len(checkInvite(time))) <= 0:
        return mongo.db.Invite.update_one(
            {"id": id, "m_id": m_id},
            {
                "$set": {
                    "name": name,
                    "friend": friend,
                    "time": timeFormat(time),
                    "remark": remark,
                }
            },
        )
    else:
        return "無法新增"


def getinviteDetail(i_id):  # 邀約詳細資料
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {"$match": {"i_id": i_id}},
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "user_id",
                        "foreignField": "id",
                        "as": "result",
                    }
                },
                {"$unwind": {"path": "$result"}},
                {
                    "$addFields": {
                        "userName": "$result.name",
                        "targetSets": "$result.target_sets",
                    }
                },
                {"$unset": ["result", "_id"]},
            ]
        )
    )


def invitelist(user_id, accept):
    # 0全部; 1接受; 2不接受; 3未回應;
    modePipline = {"user_id": user_id, "$expr": {"$lte": [{"$size": "$done"}, 0]}}
    if accept != 0:
        modePipline["accept"] = accept
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {"$match": modePipline},
                {
                    "$lookup": {
                        "from": "Invite",
                        "localField": "i_id",
                        "foreignField": "id",
                        "as": "invite",
                    }
                },
                {"$unwind": {"path": "$invite"}},
                {
                    "$addFields": {
                        "name": "$invite.name",
                        "m_id": "$invite.m_id",
                        "remark": "$invite.remark",
                        "time": "$invite.time",
                        "friend": "$invite.friend",
                    }
                },
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "m_id",
                        "foreignField": "id",
                        "as": "user",
                    }
                },
                {
                    "$unwind": {
                        "path": "$user",
                    }
                },
                {"$addFields": {"m_name": "$user.name"}},
                {"$unset": ["user", "invite", "_id"]},
                {"$sort": {"time": -1}},
                {
                    "$addFields": {
                        "time": {
                            "$dateToString": {
                                "format": timeformatString,
                                "date": "$time",
                            }
                        }
                    }
                },
            ]
        )
    )


def replyinvite(m_id, i_id, accept):
    return mongo.db.Invite_detail.update_one(
        {"i_id": i_id, "user_id": m_id},
        {
            "$set": {
                "accept": accept,
            }
        },
    )


def searchInvite(m_id, time):
    return list(
        mongo.db.Invite.find({"m_id": m_id, "time": timeFormat(time)}, {"_id": 0})
    )
