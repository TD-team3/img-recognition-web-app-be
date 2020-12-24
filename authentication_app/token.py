from random import randint
from datetime import datetime

# Token class is the representation of Token Object
# A token is generate from username and password and expired after 3 hours


class Token:

    # This static function generate a token string from username and password
    #
    # Ex. of token for "root","root" credentials -> susxwsty?=231220161503
    #
    # The first part, is composed by username and password codified taking inspiration from Julius Caesar's cipher.
    # The second part, is composed with information regarding the date and time of token generation.
    #
    # @param "username" is the username to tokenize
    # @param "password" is the password to tokenize
    #
    # @return -> token string
    @staticmethod
    def generate_token(username, password):
        token_str = ""

        # combine the credentials
        auth_credentials_str = username + password

        # TOKEN FIRST PART
        last_ascii_code = 0
        for char in auth_credentials_str:
            # convert the character to ASCII number
            ascii_code = ord(char)

            # shift the character for x random positions but two consecutive characters cannot be the same
            ascii_code = ascii_code + randint(1, 5)

            # check if two consecutive characters are the same
            # in that case, generate a new character
            while True:
                if ascii_code == last_ascii_code:
                    ascii_code = ascii_code + randint(1, 5)
                else:
                    break

            last_ascii_code = ascii_code

            # convert and assign the new character to a token string
            token_str += chr(last_ascii_code)

        # TOKEN SECOND PART

        # add separator
        token_str += "?="

        # add date time information
        token_str += "{0}".format(datetime.now().strftime("%d%m%y%H%M%S"))

        return token_str

    # Check if a token is expired
    # @param "token_str" is the token to check
    #
    # @return -> "true" if the token is expired (more than 3 hours) or the token format is not valid
    # @return -> "false" if the token is valid and isn't expired
    @staticmethod
    def is_token_expired(token_str):
        # check if token format is valid
        if Token.is_token_format_valid(token_str):
            # extract second part from the token (data information)
            expired_time_str = token_str.partition("?=")[2]

            expired_time_obj = datetime.strptime(expired_time_str, "%d%m%y%H%M%S")
            now_time_obj = datetime.now()

            # calculate time difference
            time_difference = now_time_obj - expired_time_obj

            # if token has more than 3 hours (10.800 seconds)
            if time_difference.total_seconds() > 10800:
                # token is expired
                return True
            else:
                # token is valid and not expired
                return False
        else:
            # token format is not valid
            return False

    # Check if a token format is valid
    # @param "token_str" is the token to check
    #
    # @return -> "true" if the token format is correct
    # @return -> "false" if the token format is not valid
    @staticmethod
    def is_token_format_valid(token_str):
        # extract the second part from token
        time_str = token_str.partition("?=")[2]

        # check the validity of second part
        try:
            datetime.strptime(time_str, "%d%m%y%H%M%S")
            return True
        except ValueError:
            return False


