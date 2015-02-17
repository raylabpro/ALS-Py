from app import jsonrpc
from app.lib import auth, log_db
from flask import g


@jsonrpc.method('Log.add(category=str, level=str, message=str, timestamp=int, expires_at=int) -> str', validate=True)
@auth.requires_rpc_auth
def addLog(category, level, message, timestamp, expires_at):
    log_id = log_db.addLog(g.auth.username, category, level, message, timestamp, expires_at)
    return { "logId": format(log_id) }


@jsonrpc.method('Log.getAll(category=str) -> list', validate=True)
@auth.requires_rpc_auth
def getLogAll(category):
    logs = log_db.getLogAll(g.auth.username, category)
    return {"logList": log_db.prepareData(logs) }


@jsonrpc.method('Log.getCount(category=str) -> list', validate=True)
@auth.requires_rpc_auth
def getLogCount(category):
    log_count = log_db.getLogCount(g.auth.username, category)
    return { "logCount": int(log_count) }
