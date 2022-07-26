from django.db import models

# Create your models here.


class MyDashOne(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=1000)
    engineIsSafe = models.BooleanField()

class ScrapedData(models.Model):
    username = models.CharField(max_length=120)
    channel = models.CharField(max_length=120)
    last_login = models.CharField(max_length=120)
    user_agent = models.CharField(max_length=120)
