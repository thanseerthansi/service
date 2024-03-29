
from django.db import models
from serviceapp.models import ServiceModel,ServiceCitiesModel  
# from serviceapp.serializers import 
from userapp.models import QuoteModel, UserModel

# Create your models here.
class CompanyModel(models.Model):
    company_name = models.CharField(max_length=100)
    no_of_empoyees = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=12)
    phone_number = models.CharField(max_length=12,null=True)
    email = models.EmailField(max_length=100)
    website = models.CharField(max_length=100)
    cities = models.ManyToManyField(ServiceCitiesModel)
    services = models.ManyToManyField(ServiceModel)
    status = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    created_date =  models.DateTimeField(auto_now_add=True,null=True)

class PartnerServiceModel(models.Model): #give datas as array many =true(while adding service the city add to the city model and the city add to specific service table city fieid(m2m)and remove while delete.)
    partnerid = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True)
    company_name = models.CharField(max_length=100)
    service = models.ForeignKey(ServiceModel,on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    quote = models.BooleanField(default=False)
    booking = models.BooleanField(default=False)
    price = models.CharField(max_length=100,null=True)
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)

class NotificationModel(models.Model): #create automatically when adding quote
    # partnerid = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True)
    partnerid = models.ManyToManyField(UserModel)
    quote = models.ForeignKey(QuoteModel,on_delete=models.CASCADE,null=True)
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)

class AcceptedQuoteModel(models.Model): #added while partner accept the quote and booking request
    partnerid = models.ForeignKey(PartnerServiceModel,on_delete=models.CASCADE,null=True)
    quote = models.ForeignKey(QuoteModel,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=100)
    is_booking = models.BooleanField(default=False)
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)


    
class PaymentModel(models.Model): #secretkey:: bb2K8X1SMPpvS1keCbRKTz8I ,keyid ::rzp_test_mSeuLnKB76I9N8
    quote = models.ForeignKey(AcceptedQuoteModel,on_delete=models.PROTECT)
    paymentid = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    description = models.TextField()
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)