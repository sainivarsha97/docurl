from django.db import models
# Create your models here.

class Content(models.Model):
    url = models.CharField(max_length=10)
    content = models.CharField(max_length=1000)
    title=models.CharField(max_length=30,null=True,blank=True)
    password=models.CharField(max_length=30,null=True,blank=True)
    ip=models.CharField(max_length=40,null=True,blank=True)