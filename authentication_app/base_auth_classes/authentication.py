from registration_app.models import Users
from django.core.exceptions import MultipleObjectsReturned
from datetime import datetime, timedelta
import jwt
import json


# creating Authentication class
# this will be used by the login function that will be created in views.py
# this class will include methods for checking username and password
# the class will also have to store the token


class AuthenticationJwt:

    SECRET_KEY = 'TD_team_3_Secret_Key'

    def __init__(self):
        self.token = {}

    def is_auth_data_valid(self, username, password):
        # get user from db
        try:
            user = Users.objects.get(mail=username)
        except Users.DoesNotExist:
            print("User does not exist!")
            return False

        except MultipleObjectsReturned:
            print("Internal server error! There are more users with the same username!")
            return False

        except Exception as ex:
            print("Authentication method, exception in is_auth_data_valid!")
            print(ex.args)

        # check if password is valid
        if user.password == password:
            return True
        return False

    def generate_and_save_jwt(self, username):
        payload = {'mail': username, 'iat': datetime.now(), 'exp': datetime.now() + timedelta(minutes=120)}
        # the payload will be encoded and added as a key
        encoded_jwt = jwt.encode(payload, AuthenticationJwt.SECRET_KEY, algorithm="HS256")
        json_str = "{'token':'" + str(encoded_jwt) + "'}"  # replaced json dumps
        # saving jwt into database
        #self.save_token(username, encoded_jwt)

        return json_str

    @staticmethod
    def save_token(username, jwt_token):
        # it saves jwt onto database
        Users.objects.filter(mail=username).update(token=jwt_token)


# global variable
auth = AuthenticationJwt()


