import json
from model.util import group
from model.db import mongo
from datetime import datetime, timedelta
import numpy as np


def addPlan(plan):  
    return mongo.db.plan.insert_one(plan)


def getPlan(user_id):
    return list(mongo.db.plan.find({"id": user_id}, {"_id": 0}))[0]


def editPlan(plan, user_id):
    return mongo.db.plan.update_one(
        {"id": user_id},
        {"$set": plan},
    )

# def delPlan(plan_id)
