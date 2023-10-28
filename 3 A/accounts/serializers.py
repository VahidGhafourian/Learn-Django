from rest_framework import serializers
from .models import User, OtpCode


def clean_email(value):
    if 'admin' in value:
        raise serializers.ValidationError('admin cant be in admin')


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'password2')

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (clean_email,)}
        }

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError("username can't be admin")
        elif len(value)<6:
            raise serializers.ValidationError("username should be at least 6 characters")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords must mach')
        return data


class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = '__all__'

    def create(self, validated_data):
        return OtpCode.objects.create(**validated_data)


