import json
from model.util import group
from model.db import mongo


def login(account, password):
    print(account,password)
    return list(mongo.db.user.find({"account":account,"password":password},{"_id":0}))


#def findPasswordByAccount(account, password):
    # sqlstr = f"select * from user where id=\"{account}\" and password=md5(\"{psw}\")"
    # return DB.execution(DB.select, sqlstr)
    #print(account,password)
    #return list(mongo.db.user.find({"account":account,"password":password},{"_id":0}))


def changePassword(account, password):

    return mongo.db.user.update_one({"account":account},{"$set": { "password": password }})


def sign(target):
    return mongo.db.user.insert_one(target)


def hasUser(account):
    return list(mongo.db.user.find({"account":account}))

