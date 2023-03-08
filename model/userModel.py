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


# def sign(account, password, age, gender, area, name, degree,phone):
#     sqlstr = f"insert into user(id, password,birthday,gender,area_id,name,degree,phone) VALUES (\"{account}\", md5(\"{password}\") ,\"{age}\" ,\"{gender}\",\"{area}\",\"{name}\",\"{degree}\",\"{phone}\")"
#     return DB.execution(DB.create, sqlstr)


# def hasUser(userid):
#     sqlstr = f"select count(*) as c from user where id=\"{userid}\""
#     return DB.execution(DB.select, sqlstr)

