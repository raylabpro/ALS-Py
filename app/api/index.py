from app import jsonrpc
from app.lib import auth, log_db
from flask import g
from flask_jsonrpc.exceptions import InvalidCredentialsError, OtherError, InvalidParamsError


@jsonrpc.method('Log.add(category=String, level=String, message=String, timestamp=Number, expires_at=Number) -> String',
                validate=True)
@auth.requires_rpc_auth
def addLog(category, level, message, timestamp, expires_at):
    log_id = log_db.addLog(g.auth.username, category, level, message, timestamp, expires_at)
    return {"logId": str(log_id)}


@jsonrpc.method(
    'Log.addCustom(category=String, level=String, message=String, timestamp=Number, expires_at=Number, tags=Array, additional_data=Object) -> String',
    validate=True)
@auth.requires_rpc_auth
def addCustomLog(category, level, message, timestamp, expires_at, tags, additional_data):
    log_id = log_db.addCustomLog(g.auth.username, category, level, message, timestamp, expires_at, tags,
                                 additional_data)
    return {"logId": str(log_id)}


@jsonrpc.method(
    'Log.get(category=String, search_filter=Object, limit=Number, offset=Number, sort_field=String, sort_type=String) -> Array',
    validate=True)
@auth.requires_rpc_auth
def getLog(category, search_filter={}, limit=100, offset=0, sort_field="timestamp",
           sort_type="ASCENDING"):  # or DESCENDING
    if type(sort_field) is not unicode or type(sort_type) is not unicode:
        raise InvalidParamsError("Wrong sort params!")
    logs = log_db.getLog(g.auth.username, category, search_filter, limit, offset, sort_field, sort_type)
    return {"logList": log_db.prepareOutput(logs)}


@jsonrpc.method('Log.getCount(category=String, search_filter=Object) -> Number', validate=True)
@auth.requires_rpc_auth
def getLogCount(category, search_filter={}):
    log_count = log_db.getLogCount(g.auth.username, category, search_filter)
    return {"logCount": int(log_count)}


@jsonrpc.method('Log.transfer(old_category=String, new_category=String, search_filter=Object) -> Array', validate=True)
@auth.requires_rpc_auth
def transferLog(old_category, new_category, search_filter={}):
    result = log_db.TransferLog(g.auth.username, old_category, new_category, search_filter)
    return {"transferedLogId": result}


@jsonrpc.method('Log.modify(category=String, search_filter=Object, update_data=Object) -> Array', validate=True)
@auth.requires_rpc_auth
def modifyLog(category, search_filter={}, update_data={}):
    result = log_db.modifyLog(g.auth.username, category, search_filter, update_data)
    return {"modifiedLogId": result}


@jsonrpc.method('Log.remove(category=String, search_filter=Object) -> Array', validate=True)
@auth.requires_rpc_auth
def deleteLog(category, search_filter={}):
    result = log_db.removeLog(g.auth.username, category, search_filter)
    return {"removedLogId": result}


@jsonrpc.method('Log.getCategories() -> Array', validate=True)
@auth.requires_rpc_auth
def getCategories():
    result = log_db.getCategories(g.auth.username)
    return {"categoriesList": result}


