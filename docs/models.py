from django.db import models
# Create your models here.

class Content(models.Model):
    url = models.CharField(max_length=10)
    content = models.TextField()
    title=models.CharField(max_length=50)
    password=models.CharField(max_length=16)
    ip=models.CharField(max_length=40)