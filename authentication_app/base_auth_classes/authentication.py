from .token import Token
from registration_app.models import Users

# creating Authentication class
# this will be used by the login function that will be created in views.py
# this class will include methods for checking username and password 
# the class will also have to store the token


class Authentication:
    # USERNAME = 'tdteam3'
    # PASSWORD = 'whatever'
    
    def __init__(self):
        self.token = {}

    def is_auth_data_valid(self, username, password):
        # get user from db
        try:
            user = Users.objects.get(mail=username)
        except Exception as ex:
            print("Authentication method, exception in is_auth_data_valid!")
            print(ex.args)
            return False

        # check if password is valid
        if user.password == password:
            token_str = Token.generate_token(username, password)
            # generated token string gets saved as value of the username key of the token attribute
            self.token[username] = token_str
            return True
        return False

    def is_token_valid(self, username, token_str):
        if username in self.token:
            if token_str == self.token[username]:
                if not Token.is_token_expired(token_str):
                    return True
        return False


# global variable
auth = Authentication()


