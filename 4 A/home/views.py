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

    def post(self, request):
        srz_data = QuestionSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        srz_data = QuestionSerializer(instance=question,data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Question.objects.get(pk=pk).delete()
        return Response({'message': 'question deleted'}, status=status.HTTP_200_OK)
