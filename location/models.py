from django.db import models

# Create your models here.
class States(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tblstates'

class Districts(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    state = models.ForeignKey(States, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tbldistricts'

class Tehsils(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    district = models.ForeignKey(Districts, on_delete = models.CASCADE)
    state = models.ForeignKey(States, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tbltehsils'

class Towns(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    tehsil = models.ForeignKey(Tehsils, on_delete = models.CASCADE)
    district = models.ForeignKey(Districts, on_delete = models.CASCADE)
    state = models.ForeignKey(States, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tbltowns'
