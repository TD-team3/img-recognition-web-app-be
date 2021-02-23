from datetime import datetime, timedelta
import jwt
import json
import os

# creating Authentication class
# this will be used by the login function created in views.py
# this class will include methods for generating a token following the JWT standard


class TokenJwt:

    @staticmethod
    def generate_jwt(username):
        payload = {'mail': username, 'iat': datetime.now(), 'exp': datetime.now() + timedelta(minutes=120)}
        # the payload will be encoded and added as a key
        encoded_jwt = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256")
        # saves encoded jwt onto database by calling a method of the Users model
        return encoded_jwt

    @staticmethod
    def jwt_to_json_jwt(jwt):
        # builds json with jwt inside it
        json_str = json.dumps({'token': str(jwt)})
        return json_str




