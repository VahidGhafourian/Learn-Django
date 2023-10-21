from rest_framework import serializers

class PersonSerializer(serializers.Serializer):
    # It isn't necessary to defile all attributes of model
    id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    # email = serializers.EmailField()