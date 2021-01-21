from django.db import models


class Users(models.Model):

    # ID primary key field is added automatically by Django
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=15)

    class Meta:
        db_table = "users"
