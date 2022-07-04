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


# class ServicelinkSerializer(serializers.ModelSerializer):
    
#     service_type = serializers.SerializerMethodField()
#     services = ServiceSerializer(many=True)
#     class Meta:
#         model = ServicelinkModel
#         fields = '__all__'

#     def get_service_type(self,obj):
#         print("obj1213",obj)     
#         v_obj = ServiceTypeModel.objects.filter(id=obj.service_type.id)
#         print("vobj",v_obj)
#         v_qs = ServiceTypeSerializer(v_obj, many=True)
#         return v_qs.data
    # def get_services(self,obj):    
    #     print ("objofservice",obj) 
    #     # print("services",obj.services.id)
    #     v_obj = ServiceModel.objects.filter(id=obj.services.id)
    #     v_qs = ServiceSerializer(v_obj, many=True)
        
    #     return v_qs.data