from rest_framework import serializers
from .models import User, OtpCode

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = '__all__'
