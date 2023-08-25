import json
from model.util import group
from model.db import mongo


def login(id, password):
    try:
        return list(
            mongo.db.user.find({"id": f"{id}", "password": f"{password}"}, {"_id": 0})
        )
    except:
        return "error"
def changeProfile(id,data:dict):
    return mongo.db.user.update_one({"id":id},{"$set":data})


# def findPasswordByAccount(account, password):
# sqlstr = f"select * from user where id=\"{account}\" and password=md5(\"{psw}\")"
# return DB.execution(DB.select, sqlstr)
# print(account,password)
# return list(mongo.db.user.find({"account":account,"password":password},{"_id":0}))


def changePassword(account, password):
    return mongo.db.user.update_one(
        {"account": account}, {"$set": {"password": password}}
    )


def sign(target):
    return mongo.db.user.insert_one(target)


def hasUser(account):
    try:
        return list(mongo.db.user.find({"account": account}))
    except:
        return "error"


def addpatient(data):
    try:
        mongo.db.patient.insert_one(data)
        return ""
    except:
        return "error"