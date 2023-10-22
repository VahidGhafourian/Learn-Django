from rest_framework import serializers

class UserEmailNameRelationField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.username} - {value.email}'
