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
