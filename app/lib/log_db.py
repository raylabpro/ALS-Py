import pymongo
import datetime
import time
import calendar
from app import appLogging
from config import MONGODB_HOST, MONGODB_PORT
from flask_jsonrpc.exceptions import InvalidCredentialsError, OtherError, InvalidParamsError
from bson.objectid import ObjectId

def connectCollection(db, collection, need_index=True):
    try:
        mongo = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
    except:
        raise OtherError("Unable to connect to the server")
    try:
        mongodb = mongo[db] # or mongodb = mongo.test_database
    except:
        raise OtherError("Unable to connect to db")
    try:
        mongodbc = mongodb[collection] # or mongodbc = mongodb.test_collection
    except:
        raise OtherError("Unable to connect to the collection")
    if need_index:
        mongodbc.ensure_index("expiresAt", expireAfterSeconds=0)
    return mongodbc



def addLog(db, collection, level, message, timestamp, expires_at, tags=[], additional_data={}):
    mongodbc = connectCollection(db, collection)
    expire_date = datetime.datetime.fromtimestamp(expires_at)
    log_id = mongodbc.insert({"level": level, "message": message, "timestamp": timestamp, "expiresAt": expire_date })
    return log_id


def addCustomLog(db, collection, level, message, timestamp, expires_at, tags=[], additional_data={}):
    mongodbc = connectCollection(db, collection)
    expire_date = datetime.datetime.fromtimestamp(expires_at)
    log_id = mongodbc.insert({"level": level, "message": message, "timestamp": timestamp, "expiresAt": expire_date, "tags": tags, "additionalData": additional_data })
    return log_id
    

def getLog(db, collection, search_filter={}, limit=1, offset=0, sort_field="timestamp", sort_type="ASC"): #or DESC
    if limit > 1000:
        limit = 1000
    if sort_type is "ASC":
        sort_type=pymongo.ASCENDING
    elif sort_type is "asc":
        sort_type=pymongo.ASCENDING
    else:
        sort_type=pymongo.DESCENDING
    mongodbc = connectCollection(db, collection, search_filter)
    return mongodbc.find(prepareSearchFilter(search_filter)).sort(sort_field, sort_type).limit(limit).skip(offset)


def getLogCount(db, collection, search_filter={}):
    mongodbc = connectCollection(db, collection)
    return mongodbc.find(prepareSearchFilter(search_filter)).count()


def TransferLog(db, old_category, new_category, search_filter={}):
    mongodbc_old = connectCollection(db, old_category)
    mongodbc_new = connectCollection(db, new_category)
    docs = mongodbc_old.find(prepareSearchFilter(search_filter))
    docs_to_insert = []
    docs_to_delete = []
    docs_transfered_ids = []
    if docs.count() < 1:
        return []
    for doc in list(docs):
         docs_transfered_ids.append( str(doc['_id']) )
         docs_to_insert.append( doc );
         docs_to_delete.append( ObjectId(doc['_id']) )
    mongodbc_new.insert(docs_to_insert)
    mongodbc_old.remove( {'_id':{'$in': docs_to_delete}} )
    return docs_transfered_ids


def modifyLog(db, collection, search_filter={}, update_data={}):
    mongodbc = connectCollection(db, collection)
    return mongodbc.find(prepareSearchFilter(search_filter)).count()


def removeLog(db, collection, search_filter={}):
    mongodbc = connectCollection(db, collection)
    logs = mongodbc.find(prepareSearchFilter(search_filter))
    count = logs.count()
    logs.remove()
    return count


def prepareOutput(data=list):
    result=[]
    for element in data:
        element["_id"] = str(element["_id"])
        if element["expiresAt"] is not None:
            element["expiresAt"] = time.mktime(element["expiresAt"].timetuple())
        result.append(element)
    return result

def prepareSearchFilter(search_filter):
    if '_id' in search_filter:
        if type(search_filter['_id']) is unicode:
            search_filter['_id'] = ObjectId(str(search_filter['_id']))
        if type(search_filter['_id']) is dict:
            for key, value in search_filter['_id'].iteritems():
                if type(value) is list:
                    tmp_list = search_filter['_id'][key]
                    search_filter['_id'][key] = []
                    for element in tmp_list:
                        search_filter['_id'][key].append(ObjectId(element))
        if type(search_filter['_id']) is list:
            tmp_list = search_filter['_id']
            search_filter['_id'] = []
            for element in tmp_list:
                search_filter['_id'].append(ObjectId(element))
    return search_filter