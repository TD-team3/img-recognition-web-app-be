from registration_app.models import Users
from django.core.exceptions import MultipleObjectsReturned
from authentication_app.base_auth_classes.authentication import TokenJwt

import os


class UsersManager:

    @staticmethod
    def add_new_user(mail, name, surname, password):
        # checking if email already exists in database
        check_mail = Users.objects.filter(mail=mail)

        # if the email filter leads to some result, then user already exists in database
        if check_mail.count() != 0:
            return False, 'user already registered'

        # create a new users object
        user = Users(
            mail=mail,
            name=name,
            surname=surname,
            password=password
        )

        # save user in db
        user.save()

        return True, 'user created successfully'

    @staticmethod
    def is_auth_data_valid(mail, password):
        # get user from db
        try:
            user = Users.objects.get(mail=mail)
        except Users.DoesNotExist:
            print("User does not exist")
            return False, 'User does not exist'

        except MultipleObjectsReturned:
            print("Internal server error! There are more users with the same username")
            return False, 'Internal server error! There are more users with the same username'

        except Exception as ex:
            print("Authentication method, exception in is_auth_data_valid")
            print(ex.args)

        # check if password is valid
        if user.password == password:
            return True, 'password valid'

        return False, ''

    @staticmethod
    def save_token(mail, jwt_token):
        """
        @param mail --> str
        @param jwt_token is the encoded jwt --> str
        """
        # it saves jwt encoded string onto database
        Users.objects.filter(mail=mail).update(token=jwt_token)

    @staticmethod
    def login_user(mail, password):
        key = os.environ.get('TEST')
        print(key)
        # the following checks if username is present in database and if password is correct
        status, desc = UsersManager.is_auth_data_valid(mail, password)

        if status:
            # once checked, a method gets invoked to return the json with the jwt inside it
            jwt_token = TokenJwt.generate_jwt(mail)
            UsersManager.save_token(mail, jwt_token)

            return True, TokenJwt.jwt_to_json_jwt(jwt_token)
        else:
            return False, 'authentication not valid'