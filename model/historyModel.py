import json
from model.util import group
from model.db import mongo
from datetime import datetime, timedelta
import numpy as np


def getList(id):  # 新增邀約
    return list(
        mongo.db.history.aggregate(
            [
                {"$match": {"id": id}},
                {"$project": {"_id": 0}},
            ]
        )
    )
