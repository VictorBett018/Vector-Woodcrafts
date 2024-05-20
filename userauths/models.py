from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15, null= True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=500, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
