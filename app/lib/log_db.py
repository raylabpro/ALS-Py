import pymongo
import datetime
import calendar
from config import MONGODB_HOST, MONGODB_PORT
from flask_jsonrpc.exceptions import InvalidCredentialsError

def connectCollection(db, collection):
    try:
        mongo = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
    except:
        raise InvalidCredentialsError("Error: Unable to connect to the server")
    try:
        mongodb = mongo[db] # or mongodb = mongo.test_database
    except:
        raise InvalidCredentialsError("Error: Unable to connect to db")
    try:
        mongodbc = mongodb[collection] # or mongodbc = mongodb.test_collection
    except:
        raise InvalidCredentialsError("Error: Unable to connect to the collection")

    mongodbc.ensure_index("expiresAt", expireAfterSeconds=0)
    return mongodbc



def addLog(db, collection, level, message, timestamp, expires_at):
    mongodbc = connectCollection(db, collection)
    expire_date = datetime.datetime.fromtimestamp(expires_at)
    log_id = mongodbc.insert({"level": level, "message": message, "timestamp": timestamp, "expiresAt": expire_date })
    return log_id
    

def getLog(db, collection):
    mongodbc = connectCollection(db, collection)
    # document = mongodbc.find_one({'_id': ObjectId(log_id)})
    print mongodbc.find_one()
    return true


def getLogAll(db, collection):
    mongodbc = connectCollection(db, collection)
    return mongodbc.find()


def getLogCount(db, collection):
    mongodbc = connectCollection(db, collection)
    return mongodbc.count()


def getLogCountByTag(db, collection, tag):
    mongodbc = connectCollection(db, collection)
    return mongodbc.find({"tag": tag}).count()


def getLogCountByLevel(db, collection, level):
    mongodbc = connectCollection(collection)
    return mongodbc.find({"level": level}).count()

def getLogByDate(db, collection, date_y, date_m, date_d, date_h, date_min, date_s):
    d = datetime.datetime(date_y, date_m, date_d, date_h, date_min, date_s)
    mongodbc = connectCollection(collection)
    mongodbc.find({"date": {"$lt": d}}).sort("date")


def prepareData(data):
    result=[]
    for element in data:
        element["_id"] = format(element["_id"])
        result.append(element)
    return result
