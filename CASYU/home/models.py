from django.db import models

# Create your models here.
class Signup(models.Model):
    first_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50) 
    otp=models.CharField(max_length=10)

class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')
