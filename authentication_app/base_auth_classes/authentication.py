from registration_app.models import Users
from django.core.exceptions import MultipleObjectsReturned
from datetime import datetime, timedelta


# creating Authentication class
# this will be used by the login function that will be created in views.py
# this class will include methods for checking username and password
# the class will also have to store the token


class AuthenticationJwt:
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

    def generate_token_payload(self, username):
        payload = {'mail': username, 'iat': datetime.now(), 'exp': datetime.now() + timedelta(minutes=120)}
        # consider adding the id of that database user
        return payload

    def save_token(self, username, encoded_jwt):
        self.token[username] = encoded_jwt  # the token will be saved as JWT standard encoded token


# global variable
auth = AuthenticationJwt()


