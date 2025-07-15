from rest_framework import serializers
from .models import Property

class PropertiesListSerializer(serializers.ModelSerializer):
    
    pricePerNight = serializers.CharField(source='price_per_night')
    
    class Meta:
        model = Property
        fields = {
            'id',
            'title',
            'pricePerNight',
            'image_url'
        }