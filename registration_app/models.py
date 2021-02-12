from django.db import models


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

    @property
    def full_name(self):
        return '{0} {1}'.format(self.name, self.surname)

    class Meta:
        db_table = "users"

