import json
from model.util import group, timeformatString
from model.db import mongo
from datetime import datetime, timedelta
import numpy as np


# 首頁資訊
def getHome(user_id):
    # 計算三項平均
    sportsList = list(mongo.db.Invite_detail.find({"user_id": user_id}))

    score = [0, 0, 0]
    count = [0, 0, 0]
    for i in sportsList:
        for d in i["done"]:
            print(d)
            print(type(d))
            score[d["type_id"]] = score[d["type_id"] - 1] + int(d["level"])
            count[d["type_id"]] = count[d["type_id"] - 1] + 1

    for i in range(1, len(score)):
        if count[i] != 0:
            score[i] = score[i] / count[i]

    # 取得當週運動紀錄
    firstDayOfWeek = 1
    today = datetime.now()
    currentDayOfWeek = today.weekday()

    diffToFirstDay = currentDayOfWeek - firstDayOfWeek
    if diffToFirstDay < 0:
        diffToFirstDay += 7
    start_of_week = today - timedelta(days=diffToFirstDay)
    end_of_week = start_of_week + timedelta(days=7)
    # 當週運動情形
    sportsday = list(
        mongo.db.invite_list.find({"time": {"$gte": start_of_week, "$lt": end_of_week}})
    )

    # 有哪些天要運動
    # 需增加判斷是否沒有計畫，陣列為空
    weekdays = list(list(mongo.db.plan.find({"user_id": f"{user_id}"}, {"_id": 0})))
    done_plan_list = []
    print(weekdays)

    if len(weekdays) != 0:
        for i in range(7):
            # 0 無計畫也無運動
            # 1 有計劃有運動
            # 2 有計畫無運動
            done_plan = 0
            day = start_of_week + timedelta(days=i)

            if weekdays[0]["execute"][i]:
                if any(e for e in sportsday if day in e["time"]):
                    done_plan = 1
                else:
                    done_plan = 2

            done_plan_list.append(done_plan)
    else:
        done_plan_list = [0, 0, 0, 0, 0, 0, 0]
    # 運動日程(待補，查詢invite list之後，篩選未來的資料五筆給運動日程)
    execute = list(mongo.db.Invite_detail.aggregate(
        [
            {
                "$match": {
                    "user_id": user_id,
                    "accept": 1,
                    "$expr": {"$gt": [{"$size": "$done"}, 0]},
                },
            },
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
                    "friend": "$invite.friend",
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
            {"$unset": ["user", "invite", "_id"]},
            {"$sort": {"time": -1}},
            {
                "$addFields": {
                    "time": {
                        "$dateToString": {
                            "format": timeformatString,
                            "date": "$time",
                        }
                    }
                }
            },
            {"$limit": 5},
        ])
    )
    

    return {"avg_score": score, "done_plan": done_plan_list,"execute":execute}
