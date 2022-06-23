from rest_framework import serializers

from serviceapp.serializers import *
from userapp.serializers import *
from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel 
        fields = ["company_name","no_of_empoyees","contact","email","website","description"]
       
class GetCompanySerializer(serializers.ModelSerializer):
    cities = ServiceCitiesSerializer(many=True)
    services = ServiceSerializer(many=True)
    class Meta:
        model = CompanyModel 
        fields = '__all__'
       

class PartnerServiceSerializer(serializers.ModelSerializer):
    partnerid = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    class Meta:
        model = PartnerServiceModel
        fields = '__all__'

    def get_partnerid(self,obj):
        
        v_obj = UserModel.objects.filter(id=obj.partnerid.id)
        v_qs = UserSerializer(v_obj, many=True)
        
        return v_qs.data
    
    def get_service(self,obj):
        
        v_obj = ServiceModel.objects.filter(id=obj.service.id)
        v_qs = ServiceSerializer(v_obj, many=True)
        
        return v_qs.data


class NotificationSerializer(serializers.ModelSerializer):
    # partnerid = serializers.SerializerMethodField()
    partnerid = UserSerializer(many=True)
    quote = serializers.SerializerMethodField()
    class Meta:
        model = PartnerServiceModel
        fields = '__all__'

    # def get_partnerid(self,obj):
        
    #     v_obj = UserModel.objects.filter(id=obj.partnerid.id)
    #     v_qs = UserSerializer(v_obj, many=True)
        
    #     return v_qs.data
    
    def get_quote(self,obj):
        
        v_obj = QuoteModel.objects.filter(id=obj.quote.id)
        v_qs = QuoteSerializer(v_obj, many=True)
        
        return v_qs.data


class AcceptedQuoteSerializer(serializers.ModelSerializer):
    partnerid = serializers.SerializerMethodField() 
    quote = serializers.SerializerMethodField()
    class Meta:
        model = PartnerServiceModel
        fields = '__all__'

    def get_partnerid(self,obj):
        
        v_obj = UserModel.objects.filter(id=obj.partnerid.id)
        v_qs = UserSerializer(v_obj, many=True)
        
        return v_qs.data
    
    def get_quote(self,obj):
        
        v_obj = QuoteModel.objects.filter(id=obj.quote.id)
        v_qs = QuoteSerializer(v_obj, many=True)
        
        return v_qs.data
