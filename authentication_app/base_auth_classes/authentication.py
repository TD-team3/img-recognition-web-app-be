from server.settings import SECRET_KEY
from registration_app.models import Users
from datetime import datetime, timedelta
import jwt
import json

# creating Authentication class
# this will be used by the login function created in views.py
# this class will include methods for generating a token following the JWT standard


class TokenJwt:

    @staticmethod
    def generate_and_save_jwt(username):
        payload = {'mail': username, 'iat': datetime.now(), 'exp': datetime.now() + timedelta(minutes=120)}
        # the payload will be encoded and added as a key
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        # saves encoded jwt onto database by calling a method of the Users model
        Users.save_token(username, encoded_jwt)

        return encoded_jwt

    @staticmethod
    def json_jwt(username):
        # creates and saves a JWT token based on username and current time
        encoded_jwt = TokenJwt.generate_and_save_jwt(username)
        # builds json with jwt inside it
        json_str = json.dumps({'token': str(encoded_jwt)})
        return json_str




