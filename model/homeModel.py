import json
from model.util import group
from model.db import mongo
from datetime import datetime, timedelta
import numpy as np


# 歷史運動列表
def getHome(user_id):
    sportsList = list(mongo.db.Invite_detail.find({"user_id": user_id}))

    for i in sportsList:
        score = [0, 0, 0, 0]
        count = [0, 0, 0, 0]
        for d in i["done"]:
            score[d["type_id"]] = score[d["type_id"]] + d["level"]
            count[d["type_id"]] = count[d["type_id"]] + 1
    for i in range(len(score)):
        score[i] = score[i] / count[i]
    return {"avg_score": score}
