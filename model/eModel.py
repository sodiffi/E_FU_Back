from datetime import datetime
import json
from model.util import group
from model.db import mongo


def getEpeople(e_id):
    p_list = list(mongo.db.appointment.find({"e_id": e_id}, {"_id": 0, "f_id": 1}))
    f_ids = []
    for i in p_list:
        f_ids.append(i["f_id"])
    print(f_ids)
    return list(
        mongo.db.user.aggregate(
            [
                {
                    "$match": {"id": {"$all": f_ids}},
                },
                {
                    "$lookup": {
                        "from": "patient",
                        "localField": "id",
                        "foreignField": "p_id",
                        "as": "result",
                    },
                },
                {"$unwind": "$result"},
                {
                    "$addFields": {
                        "height": "$result.height",
                        "disease": "$result.disease",
                    }
                },
                {"$unset": ["_id", "result"]},
            ]
        )
    )


def getAppoint(e_id):
    return list(
        mongo.db.appointment.aggregate(
            [
                {"$match": {"e_id": e_id}},
                {
                    "$group": {
                        "_id": {"start_date": "$start_date", "time": "$time"},
                        "count": {"$count": {}},
                    }
                },
                {"$set": {"id": "$_id"}},{"$unset":"_id"}
                
            ]
        )
    )


def getAppointDetail(e_id, start_date, time):
    return list(
        mongo.db.appointment.aggregate(
            [
                {
                    "$match": {
                        "e_id": e_id,
                        "time": time,
                        "start_date": {"$eq": datetime.fromisoformat(start_date)},
                    }
                },
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "f_id",
                        "foreignField": "id",
                        "as": "result",
                    },
                },
                {"$unwind": {"path": "$result"}},
                {"$addFields": {"name": "$result.name"}},
                {"$unset": ["result", "_id","e_id","start_date","time"]},
            ]
        )
    )
