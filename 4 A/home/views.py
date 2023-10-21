from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Person
from .serializers import PersonSerializer

class Home(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        # data = request.query_params # get data of url afte ?

        # get data with serializers
        persons = Person.objects.all()
        ser_data = PersonSerializer(instance=persons, many=True) # If you send list of objects, set many=True
        return Response(data=ser_data.data)

