from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Authentication(models.Model):
    request_token = models.CharField(max_length=25 , unique=True)
    auth_token = models.CharField(max_length=25 , unique=True , blank = True , null=True)
    redirect_url = models.URLField(max_length=200)
    user = models.ForeignKey(User , on_delete=models.CASCADE ,  blank = True , null=True , related_name="authentications")