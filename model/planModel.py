import json
from model.util import  timeFormat
from model.db import mongo
from datetime import datetime, timedelta


def addPlan(plan):
    ##新增時需判斷是否有重複區間
    if (len(checkPlan(plan["str_date"], plan["end_date"]))) <= 0:
        return mongo.db.plan.insert_one(plan)
    else:
        return "無法新增"


def checkPlan(start, end):
    return list(
        mongo.db.plan.find(
            {
                "$or": [
                    {"str_date": {"$lt": datetime.fromisoformat(start)}},
                    {"end_date": {"$gt": datetime.fromisoformat(end)}},
                ]
            }
        )
    )


def getPlan(user_id):
    return list(mongo.db.plan.find({"user_id": user_id}, {"_id": 0}))


def editPlan(plan, user_id):
    if (len(checkPlan(plan["str_date"], plan["end_date"]))) <= 0:
        return mongo.db.plan.update_one(
            {"id": user_id},
            {"$set": plan},
        )
    else:
        return "無法新增"


# def delPlan(plan_id)
