from django.db import models


# Create your models here.
class ServiceTypeModel(models.Model):
    service = models.CharField(max_length=100)
    description = models.TextField(null=True)
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)

class ServiceCitiesModel(models.Model):#while adding the partner service
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField(null=True)
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)
    
class ServiceModel(models.Model):#admin add services and cities added while adding company with patch (frontend)/
    service_type = models.ForeignKey(ServiceTypeModel,on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='Image',blank=True,null=True)
    city = models.ManyToManyField(ServiceCitiesModel)
    created_date =  models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)

