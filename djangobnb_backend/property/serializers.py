from rest_framework import serializers
from .models import Property
from useraccount.serializers import UserDetailSeralizer

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
        
class PropertiesDetailSerializer(serializers.ModelSerializer):
    landlord = UserDetailSeralizer(read_only = True, many = False)
    class Meta:
        model = Property
        fields = '__all__'