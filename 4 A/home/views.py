from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Person, Question, Answer
from .serializers import PersonSerializer, QuestionSerializer, AnswerSerializer
from rest_framework import status
from permissions import IsOwnerOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # data = request.query_params # get data of url afte ?

        # get data with serializers
        persons = Person.objects.all()
        ser_data = PersonSerializer(instance=persons, many=True) # If you send list of objects, set many=True
        return Response(data=ser_data.data)

class QuestionListView(APIView):
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        question = Question.objects.all()
        ser_data = QuestionSerializer(instance=question, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

class QuestionCreateView(APIView):
    """
        Create new question
    """
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def post(self, request):
        srz_data = QuestionSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly,]

    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        srz_data = QuestionSerializer(instance=question,data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly,]

    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        return Response({'message': 'question deleted'}, status=status.HTTP_200_OK)
