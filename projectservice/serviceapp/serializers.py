from rest_framework import serializers
from .models import *


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTypeModel 
        fields = '__all__'

class ServiceCitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCitiesModel
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    city = ServiceCitiesSerializer(many=True)
    service_type = serializers.SerializerMethodField()
    class Meta:
        model = ServiceModel
        fields = '__all__'

    def get_service_type(self,obj):
        # print("obj",obj)     
        v_obj = ServiceTypeModel.objects.filter(id=obj.service_type.id)
        
        # print("vobj",v_obj)
        v_qs = ServiceTypeSerializer(v_obj, many=True)
        
        return v_qs.data
class Service_Without_CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceModel
        fields = ["service_type","service_name"]


