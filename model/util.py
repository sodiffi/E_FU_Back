from flask import Response
import json
from coder import MyEncoder
from datetime import datetime, timedelta


timeformatString = "%Y-%m-%d T%H:%M:%S"


def timeFormat(time):
    return datetime.strptime(time, timeformatString)


def group(data: dict, tag: list, identity: str):
    """
    data 是原始資料
    tag 是要被處理成陣列的屬性
    identity是識別data是否為同一組ex id
    """
    tags = []
    ret = []
    for i in range(len(tag)):
        tags.append(set())
    check_id = -1
    temp = {}
    for i in data:
        if i[identity] != check_id:
            if check_id != -1:
                for j in range(len(tag)):
                    temp[tag[j]] = tags[j]
                ret.append(temp)
            check_id = i[identity]
            temp = i
            tags.clear()
            for j in range(len(tag)):
                tags.append(set())
            else:
                temp = i
        for j in range(len(tag)):
            tags[j].add(i[tag[j]])
    for j in range(len(tag)):
        temp[tag[j]] = tags[j]
    ret.append(temp)
    return ret


def process_date(data):
    table = ["MON", "THE", "WED", "THU", "FRI", "SAT", "SUN"]
    for i in data:
        date = i["id"]["start_date"]
        time = i["id"]["time"]

        datetime_object = datetime.strptime(f"{date}", "%Y-%m-%d %H:%M:%S")

        datetime_object += timedelta(
            days=table.index(time[0:3]), hours=int(f"0x{time[3]}", 16) + 7
        )
        i["tf_id"] = {
            "time": f'{int(f"0x{time[3]}",16)+7}:00',
            "start_date": datetime_object,
        }
        i["tf_time"] = datetime_object
    return data


def process_date_p(data):
    table = ["MON", "THE", "WED", "THU", "FRI", "SAT", "SUN"]
    for i in data:
        date = i["start_date"]
        time = i["time"]

        datetime_object = datetime.strptime(f"{date}", "%Y-%m-%d %H:%M:%S")

        datetime_object += timedelta(
            days=table.index(time[0:3]), hours=int(f"0x{time[3]}", 16) + 7
        )
        i["tf_time"] = datetime_object
    return data


