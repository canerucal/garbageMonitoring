from unicodedata import decimal
from django.db import models

# Create your models here.
class garbageLog(models.Model):
    eventID = models.AutoField(primary_key=True)
    trashID = models.IntegerField()
    creationDate = models.DateField()
    ratio = models.FloatField()

    class Meta:
        db_table = 'garbageLog'

    def __str__(self) -> str:
        return f"{self.eventID} | {self.trashID} ({self.creationDate}) {self.ratio}"