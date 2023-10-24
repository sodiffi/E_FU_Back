import json
from model.util import group
from model.db import mongo
from datetime import datetime, timedelta
import numpy as np


# 首頁資訊
def getHome(user_id):
    #計算三項平均
    sportsList = list(mongo.db.Invite_detail.find({"user_id": user_id}))

    for i in sportsList:
        score = [0, 0, 0, 0]
        count = [0, 0, 0, 0]
        for d in i["done"]:
            score[d["type_id"]] = score[d["type_id"]] + d["level"]
            count[d["type_id"]] = count[d["type_id"]] + 1
    for i in range(len(score)):
        score[i] = score[i] / count[i]

    #取得當週運動紀錄(mongodb 需撰寫invite list view table)
    firstDayOfWeek = 1
    today = datetime.now()
    currentDayOfWeek = today.date()

    diffToFirstDay = currentDayOfWeek - firstDayOfWeek
    if diffToFirstDay < 0:
        diffToFirstDay += 7
    start_of_week = today - timedelta(days=diffToFirstDay)
    end_of_week = start_of_week + timedelta(day=7)

    sportsday = list(
        mongo.db.Invite_detail.events.find(
            {"time": {"$gte": start_of_week, "$lt": end_of_week}}
        )
    )
    weekdays = list(mongo.db.plan.find({"user_id": user_id}))[0]
    done_plan_list = []
    for i in range(7):
        # 0 無計畫也無運動
        # 1 有計劃有運動
        # 2 有計畫無運動
        done_plan = 0
        day = start_of_week + timedelta(days=i)

        if weekdays[i]:
            if any(e for e in sportsday if day in e["time"]):
                done_plan = 1
            else:
                done_plan = 2

        done_plan_list.append(done_plan)
    
    #運動日程(待補，可與當週運動紀錄合併，查詢invite list之後，篩選當週之後的資料，當週給當週運動，未來的資料給運動日程)
    
    return {"avg_score": score,"done_plan":done_plan_list}
