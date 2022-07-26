from flask_restful import Resource, reqparse
from models.user import UserModel
from blacklist import BLACKLIST

from hmac import compare_digest
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity

parser = reqparse.RequestParser()
parser.add_argument(
    'username',
    type=str,
    required=True,
    help="This field cannot be blank"
)
parser.add_argument(
    'password',
    type=str,
    required=True,
    help="This field cannot be blank"
)



class UserRegister(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists!"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}
        user.delete_from_db()
        return {'message': "User deleted"}

class UserLogin(Resource):
    @classmethod
    def post(self):
        # get data from parser
        data = parser.parse_args()
        # find user in database
        user = UserModel.find_by_username(data['username'])
        # check password
        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, 200
        return {"message": "invalid credentials"}, 401
        # create access token
        # create refresh token

class UserLogout(Resource):
    #blacklist the current access token because upon logging in again a new access token will be generated
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {'message': f'User <id={user_id}> successfully logged out.'}

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200