from array import ArrayType
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Currencies(models.Model):
    currencies = ArrayField(models.CharField(max_length=100))
    period = ArrayField(models.CharField(max_length=200), size=2)
    sortingOrder = models.CharField(max_length=100)
    
