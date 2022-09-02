from django.db import models
from django.contrib.auth.models import User
import random
from django.utils.crypto import get_random_string

def my_function():
  return get_random_string(length = random.randint(20,25))


# Create your models here.
class Authentication(models.Model):
    request_token = models.CharField(max_length=25 , unique=True , default = my_function)
    auth_token = models.CharField(max_length=25 , unique=True , blank = True , null=True)
    redirect_url = models.URLField(max_length=200)
    user = models.ForeignKey(User , on_delete=models.CASCADE ,  blank = True , null=True , related_name="authentications")