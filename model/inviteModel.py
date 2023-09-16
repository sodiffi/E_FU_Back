import json
from model.util import group
from model.db import mongo
from datetime import datetime, timedelta
import numpy as np


def addinvite(id, name, m_id, friend, time, remark):  # 新增邀約
    return mongo.db.Invite.insert_one(
        {
            "id": id,
            "name": name,
            "m_id": m_id,
            "friend": friend,
            "time": time,
            "remark": remark,
        }
    )


def addinvitedetail(data):
    return mongo.db.Invite_detail.insert_many(data)


def editinvite(id, name, m_id, friend, time, remark):  # 修改邀約
    return mongo.db.Invite.update_one(
        {"id": id, "m_id": m_id},
        {"$set": {"name": name, "friend": friend, "time": time, "remark": remark}},
    )


def getacceptID(m_id):  # 已接受的邀約ID
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {"$match": {"user_id": m_id, "accept": True}},
                {"$project": {"id": "$a_id", "_id": 0}},
            ]
        )
    )


# 邀約列表 - 接受
def getacceptList(m_id, acceptList):
    return list(
        mongo.db.Invite.aggregate(
            [
                {"$match": {"m_id": m_id}},
                {"$project": {"id": 1, "name": 1, "time": 1, "_id": 0}},
                {
                    "$unionWith": {
                        "coll": "Invite",
                        "pipeline": [
                            {"$match": {"id": {"$in": acceptList}}},
                            {"$project": {"id": 1, "name": 1, "time": 1, "_id": 0}},
                        ],
                    }
                },
                {"$sort": {"time": 1}},
            ]
        )
    )


# 邀約列表 - 拒絕
def getrejectID(m_id):
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {"$match": {"user_id": m_id, "accept": False}},
                {"$project": {"id": "$a_id", "_id": 0}},
            ]
        )
    )


def getrejectList(rejectList):
    return list(
        mongo.db.Invite.aggregate(
            [
                {"$match": {"id": {"$in": rejectList}}},
                {"$project": {"id": 1, "name": 1, "time": 1, "_id": 0}},
                {"$sort": {"time": 1}},
            ]
        )
    )


# 邀約列表 - 未回應
def getunreplyID(m_id):
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {"$match": {"user_id": m_id, "accept": np.nan}},
                {"$project": {"id": "$a_id", "_id": 0}},
            ]
        )
    )


def getunreplyList(unreplyList):
    return list(
        mongo.db.Invite.aggregate(
            [
                {"$match": {"id": {"$in": unreplyList}}},
                {"$project": {"id": 1, "name": 1, "time": 1, "_id": 0}},
                {"$sort": {"time": 1}},
            ]
        )
    )


# 邀約列表 - 全部
def getinviteList(m_id, acceptList, rejectList, unreplyList):
    return list(
        mongo.db.Invite.aggregate(
            [
                {"$match": {"m_id": m_id}},
                {"$project": {"id": 1, "name": 1, "time": 1, "_id": 0}},
                {
                    "$unionWith": {
                        "coll": "Invite",
                        "pipeline": [
                            {"$match": {"id": {"$in": acceptList}}},
                            {
                                "$project": {
                                    "id": 1,
                                    "name": 1,
                                    "time": 1,
                                    "_id": 0,
                                }
                            },
                        ],
                    }
                },
                {
                    "$unionWith": {
                        "coll": "Invite",
                        "pipeline": [
                            {"$match": {"id": {"$in": rejectList}}},
                            {
                                "$project": {
                                    "id": 1,
                                    "name": 1,
                                    "time": 1,
                                    "_id": 0,
                                }
                            },
                        ],
                    }
                },
                {
                    "$unionWith": {
                        "coll": "Invite",
                        "pipeline": [
                            {"$match": {"id": {"$in": unreplyList}}},
                            {
                                "$project": {
                                    "id": 1,
                                    "name": 1,
                                    "time": 1,
                                    "_id": 0,
                                }
                            },
                        ],
                    }
                },
                {"$sort": {"time": 1}},
            ]
        )
    )
    # return list(mongo.db.Invite.aggregate(
    #         [
    #             {
    #                 '$match': {
    #                     'm_id': m_id
    #                 }
    #             }, {
    #                 '$project': {
    #                     'id': 1, 'name': 1, 'time': 1, '_id': 0
    #                 }
    #             }, {
    #                 '$unionWith': {
    #                     'coll': 'Invite',
    #                     'pipeline': [
    #                         {
    #                             '$match': {
    #                                 'id': {'$in': acceptList}
    #                             }
    #                         }, {
    #                             '$project': {
    #                                 'id': 1, 'name': 1, 'time': 1, '_id': 0
    #                             }
    #                         }
    #                     ]
    #                 }
    #             }
    #         ]
    #     ))


def getinviteDetail(m_id, id):  # 邀約詳細資料
    return list(mongo.db.Invite.find({"m_id": m_id, "id": id}, {"_id": 0}))


def invitelist(user_id, id):
    # 0全部; 1接受; 2不接受; 3未回應;
    modePipline = {
        "user_id": user_id,
    }
    if id!=0:
        modePipline['accept']=  True  if id == 1 else (False if id == 2 else None)
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
                        "friend":"$invite.friend",
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
                {"$unset":["user","invite","_id"]}
            ]
        )
    )


def replyinvite(m_id, a_id, accept):
    return mongo.db.Invite_detail.update_one(
        {"a_id": a_id, "user_id": m_id},
        {
            "$set": {
                "accept": accept,
            }
        },
    )


# def reject():
#     return ''
