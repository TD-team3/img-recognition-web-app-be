from django.db import models
from django.core.exceptions import MultipleObjectsReturned


class Users(models.Model):

    # ID primary key field is added automatically by Django
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    mail = models.EmailField(max_length=254)
    password = models.CharField(max_length=15)
    token = models.CharField(max_length=250, default='')

    def __str__(self):
        return 'id:{0}, name:{1}, surname:{2}, mail:{3}, password:{4}'\
            .format(self.pk, self.name, self.surname, self.mail, self.password)
        return '%s %s' % (self.name, self.surname)

    @staticmethod
    def is_auth_data_valid(username, password):
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

    @staticmethod
    def save_token(username, jwt_token):
        """
        @param username --> str
        @param jwt_token is the encoded jwt --> str
        """
        # it saves jwt encoded string onto database
        Users.objects.filter(mail=username).update(token=jwt_token)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.name, self.surname)

    class Meta:
        db_table = "users"

