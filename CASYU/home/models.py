from email.policy import default
from django.db import models

# Create your models here.
class Signup(models.Model):
    first_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50) 
    otp=models.CharField(max_length=10)
    token=models.CharField(max_length=22)

class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')

class Signup_service(models.Model):
    first_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50) 
    otp=models.CharField(max_length=10)
    service=models.CharField(max_length=25)
    amount=models.IntegerField()
    token=models.CharField(max_length=22)

class perfect_service(models.Model):
    amt_offered=models.IntegerField()
    customer_usr=models.CharField(max_length=50)
    customer_boolean=models.CharField(max_length=1)
    service_usr=models.CharField(max_length=50)
    service_boolean=models.CharField(max_length=1)
    ser_amt_offered=models.CharField(default='NOT SEEN',max_length=10)
    final=models.IntegerField(default=0)

