from datetime import datetime, timedelta
import jwt
import json
import os
import user_manager

# creating Authentication class
# this will be used by the login function created in views.py
# this class will include methods for generating a token following the JWT standard


class TokenJwt:

    @staticmethod
    def generate_jwt(username):
        # adding iat and exp keys will automatize the expiration check
        payload = {'mail': username, 'iat': datetime.now(), 'exp': datetime.utcnow() + timedelta(seconds=20)}
        # the payload will be encoded and added as a key
        encoded_jwt = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256")
        # saves encoded jwt onto database by calling a method of the Users model
        return encoded_jwt

    @staticmethod
    def jwt_to_json_jwt(jwt):
        # builds json with jwt inside it
        json_str = json.dumps({'token': str(jwt)})
        return json_str

    @staticmethod
    def decode_json_jwt(encoded_jwt):
        # decoding the encoded jwt string
        decoded = jwt.decode(encoded_jwt, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
        return decoded

    @staticmethod
    def is_token_valid(username, encoded_jwt):
        if not encoded_jwt:
            return False, 'Empty token!'
        # retrieving the token from database
        token_in_db = user_manager.UsersManager.retrieve_token(username)
        # checking if the token corresponds
        if token_in_db == encoded_jwt:
            # decoding the db token to find the expiration
            try:
                # the decode automatically checks the expiration
                decoded_db_token = TokenJwt.decode_json_jwt(token_in_db)
            except jwt.ExpiredSignatureError:
                return False, 'Session expired!'
            return True, 'ok'
        else:
            return False, 'Invalid token!'












