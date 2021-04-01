from django.db import models
from registration_app.models import Users


# Create your models here.
class History(models.Model):
    # Auto incremental ID is automatically set by Django ORM
    rcg_output = models.CharField(max_length=300)
    datetime = models.DateTimeField()

    mail = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        db_table = "history"

    def __str__(self):
        return 'id:{0}, rcg_output:{1}, datetime:{2}, mail:{3}'\
            .format(self.pk, self.rcg_output, self.datetime, self.mail, self.mail)

