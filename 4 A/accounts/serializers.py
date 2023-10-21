from rest_framework import serializers
from django.contrib.auth.models import User

def clean_email(value):
    if 'admin' in value:
        raise serializers.ValidationError('admin cant be in admin')

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User

        # fields = '__all__' # select all fields
        fields = ('username', 'email', 'password', 'password2') # select some fields with tuple
        # excludes = ('username', ) # remove some fields of selected fields. (must be some fields before this. Ex: line 9)

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (clean_email, )}
        }

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError("username can't be admin")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords must mach')
        return data
