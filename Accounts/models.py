from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Registration(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    mobile_number=models.CharField(max_length=10,default=None)
    address = models.TextField(max_length=300, blank=True,null=True)
    city = models.CharField(max_length=100, blank=True,default='Noida',null=True)
    state = models.CharField(max_length=100, blank=True,default=None,null=True)
    postal_code = models.IntegerField(blank=True,default=None,null=True)
    age=models.IntegerField(default=20,null=True)
    gender=models.CharField(max_length=10,default='Male',null=True)
    country = models.CharField(max_length=50, blank=True,default=None,null=True)
    additional_information = models.TextField(max_length=1000,null=True,blank=True)
    image=models.ImageField(upload_to='Accounts',default=None,blank=True)

    def __str__(self):
        return self.user.username
