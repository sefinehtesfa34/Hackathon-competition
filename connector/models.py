from django.db import models
from django.forms import PasswordInput


class RegisterModel(models.Model):
    email=models.EmailField(max_length=50)
    firstName=models.CharField(max_length=50,default='sefineh')
    lastName=models.CharField(max_length=50,default='tesfa')
    userName=models.CharField(max_length=50,default='sefineh')
    password=models.CharField(max_length=100,default='')
    
    
    

    
