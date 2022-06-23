# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

from serviceapp.models import ServiceModel
# Create your models here.
class UserModel(AbstractUser):
    mobile = models.CharField(max_length=100,blank=True)
    is_admin = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    

class LocationModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    location = models.PointField(geography=True, blank=True, null=True)
    place = models.CharField(max_length=100,null=True)
    area = models.CharField(max_length=100,null=True)
    street_no = models.CharField(max_length=100,null=True)
    appartment_no = models.CharField(max_length=100,null=True)

class QuoteModel(models.Model):
    userid = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True,blank=True)
    service = models.ForeignKey(ServiceModel,on_delete=models.SET_NULL,null=True)
    service_date = models.DateField()
    service_location = models.CharField(max_length=100)
    living_type = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.CharField(max_length=100)
    created_date =  models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)