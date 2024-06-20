from rest_framework import serializers
from app_service.models import Service


class ServiceSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = {
            'owner_id': {'read_only': True}
        }
        

class GetServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_price', 'service_type', 'owner_id']
