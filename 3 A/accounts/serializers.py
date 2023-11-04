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

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = '__all__'

    def create(self, validated_data):
        return OtpCode.objects.create(**validated_data)


