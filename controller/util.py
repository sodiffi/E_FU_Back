from flask import Response, jsonify, make_response
import json
from itsdangerous import TimedJSONWebSignatureSerializer as TJSS,BadSignature,SignatureExpired
from coder import MyEncoder
import app
from model.db import mongo
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

def get_next_id(collection_name):
    # 首先讀取計數器的值並遞增
    counter = mongo.db.counters.find_one_and_update(
        {'_id': collection_name},
        {'$inc': {'count': 1}},
        upsert=True,  # 如果文檔不存在，創建一個新的文檔
        return_document=ReturnDocument.AFTER
    )
    
    # 使用遞增後的計數器值來生成自增 ID
    next_id = counter['count']
    return next_id


def checkParm(cond, content, option=None):
    res = ""
    result = {}
    for i in cond:
        if(i not in content.keys()):
            res += "缺少必要參數 %s\n" % i
            break
        else:
            result[i] = content[i]
    return res if len(res) > 0 else result


def ret(result):
    # print(result)
    mes= " " if "mes"  not in result.keys() else result["mes"]
    resultData = result["data"] if "data" in result else {}
    response=make_response(json.dumps({"D": resultData, "message": mes, "success": result["success"], }, cls=MyEncoder))
    response.headers["Content-Type"] = "text/json; charset=utf-8"
    return response
def quickRet(result):
    print(result)
    print(type(result))
    mes= result if result=="error" else " "
    response = make_response(
        json.dumps(
            {
                "D": result,
                "message": mes,
                "success": type(result) == list,
            },
            cls=MyEncoder,
        )
    )
    response.headers["Content-Type"] = "text/json; charset=utf-8"
    return response

def identity(token):
    s = TJSS(app.config['SECRET_KEY'], expires_in=3600)
    data=""
    try:
        data = s.loads(token)  # 驗證
    except SignatureExpired:
        #  當時間超過的時候就會引發SignatureExpired錯誤
        print('SignatureExpired, over time')
    except BadSignature:
        #  當驗證錯誤的時候就會引發BadSignature錯誤
        print('BadSignature, No match')
    finally:
        print('finish')
    return data

    


# 好像不能用


def normalize_query_param(value):
    """
    Given a non-flattened query parameter value,
    and if the value is a list only containing 1 item,
    then the value is flattened.

    :param value: a value from a query parameter
    :return: a normalized query parameter value
    """
    return value if len(value) > 1 else value[0]


def normalize_query(params):
    """
    Converts query parameters from only containing one value for each parameter,
    to include parameters with multiple values as lists.

    :param params: a flask query parameters data structure
    :return: a dict of normalized query parameters
    """
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}
