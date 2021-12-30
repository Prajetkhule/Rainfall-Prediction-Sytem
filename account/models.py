from django.db import models

# Create your models here.
class Roles(models.Model):
    name = models.CharField(max_length = 10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tblroles'

class AppUsers(models.Model):
    fullname = models.CharField(max_length = 70)
    mobile = models.CharField(max_length = 10, unique = True)
    password = models.CharField(max_length = 20)
    role = models.ForeignKey(Roles, on_delete = models.CASCADE, default = 2)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'tblusers'
