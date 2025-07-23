from rest_framework import serializers

from .models import User

class UserDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'avatar_url']