from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Person, Question, Answer
from .serializers import PersonSerializer, QuestionSerializer, AnswerSerializer
from rest_framework import status

class Home(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        # data = request.query_params # get data of url afte ?

        # get data with serializers
        persons = Person.objects.all()
        ser_data = PersonSerializer(instance=persons, many=True) # If you send list of objects, set many=True
        return Response(data=ser_data.data)

class QuestionView(APIView):
    def get(self, request):
        question = Question.objects.all()
        ser_data = QuestionSerializer(instance=question, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
