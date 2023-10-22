from rest_framework import serializers
from .models import Question, Answer

class PersonSerializer(serializers.Serializer):
    # It isn't necessary to defile all attributes of model
    id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    # email = serializers.EmailField()

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_answers(self, obj):
        results = obj.answers.all()
        return AnswerSerializer(instance=results, many=True).data

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
