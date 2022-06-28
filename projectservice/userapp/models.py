# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from uuid import uuid4

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
    unique_code = models.CharField(max_length=100, default=datetime.now().strftime('%Y%m%d%H') + str(uuid4()),editable = False)
    service_date = models.DateField()
    service_time = models.TimeField(null=True)#for booking
    service_location = models.CharField(max_length=100)
    moveto_location =models.CharField(max_length=100,null=True)#for moving service only
    size_of_home = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.CharField(max_length=100)
    is_booking = models.BooleanField(default=False)
    payment = models.CharField(max_length=100,null=True)
    created_date =  models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class WalletModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    description = models.TextField()
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)

class CardModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    card_no = models.IntegerField()
    name_on_card = models.CharField(max_length=100)
    valid_thru = models.CharField(max_length=100)
    cvv = models.IntegerField()
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)



