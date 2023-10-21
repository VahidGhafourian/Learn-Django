from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer

class Home(APIView):
    def get(self, request):
        # data = request.query_params # get data of url afte ?

        # get data with serializers
        persons = Person.objects.all()
        ser_data = PersonSerializer(instance=persons, many=True) # If you send list of objects, set many=True
        return Response(data=ser_data.data)

    def post(self, request):
        name = request.data['name']
        return Response({
            'name': name
        })
