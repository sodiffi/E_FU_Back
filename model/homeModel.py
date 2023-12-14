import json
from model.util import group, timeformatString
from model.db import mongo
from datetime import datetime, timedelta


def is_same_day(date1, date2):
    return (
        date1.year == date2.year
        and date1.month == date2.month
        and date1.day == date2.day
    )


# 首頁資訊
def getHome(user_id):
    # 計算三項平均
    # score = list(mongo.db.user.find({"id": f"{user_id}"},{"_id":0,"sport_info":1}))[0]

    # 取得當週運動紀錄

    today = datetime.now()
    currentDayOfWeek = today.weekday()

    start_of_week = today - timedelta(days=currentDayOfWeek)
    end_of_week = start_of_week + timedelta(days=6)
    print("start", start_of_week, "end", end_of_week)
    # 當週運動情形
    sportsday = list(
        mongo.db.invite_lsit.find(
            {
                "time": {
                    "$gte": start_of_week,
                    "$lte": end_of_week,
                  
                },
                  "user_id": f"{user_id}",
            }
        )
    )
    # print("sportday",sportsday)

    # 有哪些天要運動
    # 需增加判斷是否沒有計畫，陣列為空
    weekdays = list(
        mongo.db.plan.find(
            {
                "user_id": f"{user_id}",
                "str_date": {"$lte": datetime.now()},
                "end_date": {"$gte": datetime.now()},
            },
            {"_id": 0},
        )
    )
    done_plan_list = []
    print("weekdays", weekdays)

    if len(weekdays) != 0:
        for i in range(7):
            # 0 無計畫也無運動
            # 1 有計劃有運動
            # 2 有計畫無運動
            done_plan = 0
            day = start_of_week + timedelta(days=i)

            if weekdays[0]["execute"][i]:
                if any(e for e in sportsday if is_same_day(day, e["time"])):
                    done_plan = 1
                else:
                    done_plan = 2

            done_plan_list.append(done_plan)
    else:
        done_plan_list = [0, 0, 0, 0, 0, 0, 0]
    # 運動日程(待補，查詢invite list之後，篩選未來的資料五筆給運動日程)
    execute = list(
        mongo.db.Invite_detail.aggregate(
            [
                {
                    "$match": {
                        "user_id": f"{user_id}",
                        "accept": 1,
                        "$expr": {"$lte": [{"$size": "$done"}, 0]},
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
                {"$sort": {"time": 1}},
                {
                    "$match": {
                        "time": {"$gte": datetime.today()},
                    }
                },
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
            ]
        )
    )
    print(execute)

    return {"done_plan": done_plan_list, "execute": execute}
