import json

from model.util import group
from model.db import mongo

import re


def getmoFriend(friend_ids, hidden_ids):
    return list(
        mongo.db.user.aggregate(
            [
                {
                    "$match": {"id": {"$in": friend_ids, "$nin": hidden_ids}},
                },
                {"$unset": ["_id", "password", "friend", "hide_friend"]},
            ]
        )
    )


def getHideFriendid(user_id):
    return list(mongo.db.user.find({"id": user_id}, {"_id": 0, "hide_friend": 1}))


def getHideFriendData(hidelist):
    return list(
        mongo.db.user.aggregate(
            [
                {"$match": {"id": {"$in": hidelist}}},
                {"$project": {"name": 1, "id": 1, "_id": 0}},
            ]
        )
    )


def doHideFriend(user_id, hide_id):
    return mongo.db.user.update_one(
        {"id": user_id}, {"$push": {"hide_friend": hide_id}}
    )


def doShowFriend(user_id, show_id):
    return mongo.db.user.update_one(
        {"id": user_id}, {"$pull": {"hide_friend": show_id}}
    )


def search(keyword):
    return list(
        mongo.db.user.aggregate(
            [
                {
                    "$match": {
                        "$or": [
                            {"id": re.compile(rf"{keyword}")},
                            {"name": re.compile(rf"{keyword}")},
                        ]
                    }
                },
                {"$project": {"name": 1, "id": 1, "_id": 0}},
            ]
        )
    )


def rank(user_id):
    friend = list(mongo.db.user.find({"id": user_id}))[0]["friend"]
    if isinstance(friend, list):
        friend.append(user_id)
        return list(
            mongo.db.user.aggregate(
                [
                    {
                        "$match": {"id": {"$in": friend}},
                    },
                    {"$sort": {"score": -1,"name":1}},
                    {"$unset": ["_id", "password"]},
                ]
            )
        )
    else:
        return []
    
def getAvg(user_id):
    return list(
            mongo.db.user.aggregate(
                [
                    {'$match': 
                        {'id': user_id}
                        }, 
                    {'$project': 
                        {'score': 1, '_id': 0}
                    }
                ]
            )
        )

    
def getUser(card_id):
    return list(
            mongo.db.user.aggregate(
                [
                    {'$match': 
                        {'card_id': card_id}
                    },{
                        "$project":{
                            "_id":0
                        }
                    }
                ]
            )
        )

def getRadar(user_id):
    return list(
            mongo.db.Invite_detail.aggregate(
                [
                    {'$match': {'user_id': user_id}}, 
                    {
                        '$lookup': {
                            'from': 'Invite', 
                            'localField': 'i_id', 
                            'foreignField': 'id', 
                            'as': 'invite'
                        }
                    }, 
                    {'$unwind': {'path': '$invite'}}, 
                    {'$addFields': {'time': '$invite.time', 'name': '$invite.name'}}, 
                    {'$unset': 'invite'}, 
                    {'$sort': {'time': -1}}, 
                    {'$project': {'_id': 0}}, 
                    {'$limit': 1}
                ]
            )
        )
