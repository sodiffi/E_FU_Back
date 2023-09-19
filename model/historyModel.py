import json
from model.util import group
from model.db import mongo
from datetime import datetime, timedelta
import numpy as np


# 歷史運動列表
def getList(id):
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {
                    "$match": {
                        "user_id": id,
                        "accept": True,
                        "$expr": {"$gt": [{"$size": "$done"}, 0]},
                    }
                },
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
                {"$unset": ["_id", "i_data", "m_data"]},
                {"$match": {"time": {"$lte": datetime.now()}}},
            ]
        )
    )


def getHistory(h_id):
    print(h_id)
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {
                    "$match": {
                        "i_id": int(h_id),
                    }
                },
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "user_id",
                        "foreignField": "id",
                        "as": "m_data",
                    }
                },
                {"$unwind": "$m_data"},
                {"$addFields": {"name": "$m_data.name"}},
                {"$unset": ["_id", "i_data", "m_data"]},
            ]
            # {"i_id": int(h_id)}, {"_id": 0}
        )
    )
