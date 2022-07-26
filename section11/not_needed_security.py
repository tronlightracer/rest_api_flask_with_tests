#from werkzeug.security import safe_str_cmp
from hmac import compare_digest
from models.user import UserModel


def authenticate(username, password):
    #.get() gives value of the key in paranthesis. default value is None
    user = UserModel.find_by_username(username)
    #safely compares the strings
    if user and compare_digest(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)