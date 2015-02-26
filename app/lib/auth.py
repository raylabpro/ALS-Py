import pymongo
from functools import wraps
from flask import request, Response, g
from app import jsonrpc
from flask_jsonrpc.exceptions import InvalidCredentialsError
from config import MONGODB_HOST, MONGODB_PORT
from log_db import connectCollection

def check_auth(username, password):
    """
        This function is called to check if a username / password combination is valid.
    """
    mongodbc = connectCollection("apiDB", "users", need_index=False)
    user = mongodbc.find_one({'login': username})
    if user != None:
        return user["password"] == password
    else:
        return False
    return False # just for sure

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def static_auth(username, password):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def requires_rpc_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            raise InvalidCredentialsError("You are not allowed here!")
        g.auth = auth
        return f(*args, **kwargs)
    return decorated


def static_rpc_auth(username, password):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        raise InvalidCredentialsError("You are not allowed here!")
    g.auth = auth
    return True
