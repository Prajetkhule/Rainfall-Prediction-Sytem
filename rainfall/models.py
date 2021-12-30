from django.db import models
from location.models import States
# Create your models here.
class RainfallDataset(models.Model):
    state = models.ForeignKey(States, on_delete = models.CASCADE)
    year = models.IntegerField()
    annual = models.FloatField()
    jf = models.FloatField()
    mam = models.FloatField()
    jjas = models.FloatField()
    ond = models.FloatField()

    class Meta:
        db_table = 'tblrainfall'
