import json
from model.util import timeFormat
from model.db import mongo
from datetime import datetime, timedelta


def addPlan(plan):
    ##新增時需判斷是否有重複區間
    plan["str_date"] = datetime.fromisoformat(plan["str_date"])
    plan["end_date"] = datetime.fromisoformat(plan["end_date"])
    print(plan["str_date"], plan["end_date"])
    print(checkPlan(plan["str_date"], plan["end_date"], plan["user_id"]))
    if (len(checkPlan(plan["str_date"], plan["end_date"], plan["user_id"]))) <= 0:
        return mongo.db.plan.insert_one(plan)
    else:
        return "無法新增"


def checkPlan(start: datetime, end: datetime, user_id):
    return list(
        mongo.db.plan.find(
            {
                "user_id": "11136024",
                "$or": [
                    {
                        "str_date": {
                            "$lte": end
                        },
                        "end_date": {
                            "$gte": start
                        },
                    },
                    {
                        "str_date": {
                            "$lte": start
                        },
                        "end_date": {
                            "$gte": end
                        },
                    },
                ],
            }
        )
    )


def getPlan(user_id):
    return list(mongo.db.plan.aggregate([{"$match":{"user_id": user_id}}, {"$unset":["_id"]},{"$sort":{"str_date":1}}]))
# .sort({"str_date":1})


def editPlan(plan, user_id):
    plan["str_date"] = datetime.fromisoformat(plan["str_date"])
    plan["end_date"] = datetime.fromisoformat(plan["end_date"])
    if (len(checkPlan(plan["str_date"], plan["end_date"], user_id))) <= 0:
        return mongo.db.plan.update_one(
            {"id": user_id},
            {"$set": plan},
        )
    else:
        return "無法新增"


def barChart(user_id):
    detail = list(
        mongo.db.Invite_detail.aggregate(
            [
                {
                    "$match": {
                        "user_id": user_id,
                        "accept": 1,
                        "total_score": {"$exists": True},
                    }
                },
                {"$group": {"_id": None, "id": {"$addToSet": "$i_id"}}},
                {"$project": {"_id": 0, "id": 1}},
            ]
        )
    )[0]["id"]

    twelve_months_ago = datetime.now() - timedelta(days=365)

    return list(
        mongo.db.Invite.aggregate(
            [
                {
                    "$match": {
                        "id": {"$in": detail},
                        "time": {"$gte": twelve_months_ago, "$lt": datetime.now()},
                    }
                },
                {
                    "$project": {
                        "month": {"$month": {"$toDate": "$time"}},
                        "_id": 0,
                        "id": 1,
                    }
                },
                {"$group": {"_id": "$month", "count": {"$sum": 1}}},
                {"$addFields": {"month": "$_id"}},
                {"$project": {"_id": 0}},
            ]
        )
    )


def runChart(user_id):
    return list(
            mongo.db.Invite_detail.aggregate(
                [
                    {
                        '$match': {
                            'user_id': user_id, 
                            'accept': 1, 
                            'total_score': {
                                '$exists': True
                            }
                        }
                    }, {
                        '$lookup': {
                            'from': 'Invite', 
                            'localField': 'i_id', 
                            'foreignField': 'id', 
                            'as': 'result'
                        }
                    }, {
                        '$unwind': '$result'
                    }, {
                        '$addFields': {
                            'time': '$result.time'
                        }
                    }, {
                        '$project': {
                            'result': 0
                        }
                    }, {
                        '$project': {
                            'yearMonth': {
                                '$dateToString': {
                                    'format': '%Y-%m', 
                                    'date': {
                                        '$toDate': '$time'
                                    }
                                }
                            }, 
                            'total_score': 1, 
                            '_id': 0, 
                            'id': 1
                        }
                    }, {
                        '$group': {
                            '_id': '$yearMonth', 
                            'count': {
                                '$sum': 1
                            }, 
                            'score': {
                                '$sum': '$total_score'
                            }, 
                            'avg': {
                                '$avg': '$total_score'
                            }
                        }
                    }, {
                        '$sort': {
                            '_id': 1
                        }
                    }
                ]
            )
        )
