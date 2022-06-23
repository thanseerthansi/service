from rest_framework import serializers
from serviceapp.serializers import *
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

class LocaionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = LocationModel
        fields = '__all__'
    def get_user(self,obj):
        
        v_obj = UserModel.objects.filter(id=obj.user.id)
        v_qs = UserSerializer(v_obj, many=True)
        
        return v_qs.data

class QuoteSerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    class Meta:
        model = QuoteModel
        fields = '__all__'

    def get_userid(self,obj):
        
        v_obj = UserModel.objects.filter(id=obj.userid.id)
        v_qs = UserSerializer(v_obj, many=True)
        
        return v_qs.data
    
    def get_service(self,obj):
        
        v_obj = ServiceModel.objects.filter(id=obj.service.id)
        v_qs = ServiceSerializer(v_obj, many=True)
        
        return v_qs.data
