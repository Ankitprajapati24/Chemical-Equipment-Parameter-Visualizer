from rest_framework import serializers
from .models import EquipmentFile
from django.contrib.auth.models import User

# 1. File Serializer (For Data Uploads)
class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFile
        fields = ['file']

# 2. User Serializer (For Login/Register)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        # Security: Write-only means we can accept passwords but never send them back
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # This creates a secure, hashed user account (Production Standard)
        user = User.objects.create_user(**validated_data)
        return user