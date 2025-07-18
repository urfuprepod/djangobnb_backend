from rest_framework import serializers
from .models import Property

class PropertiesListSerializer(serializers.ModelSerializer):
    
    pricePerNight = serializers.CharField(source='price_per_night')
    imageUrl = serializers.CharField(source='image_url')
    
    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'pricePerNight',
            'imageUrl'
        ]