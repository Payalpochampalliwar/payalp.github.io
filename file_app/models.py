from django.db import models

class File(models.Model):
    file = models.FileField(upload_to='files/')

class DPDCount(models.Model):
    state = models.CharField(max_length=255)
    dpd = models.IntegerField()
    count = models.IntegerField()