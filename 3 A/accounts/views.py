import random
from utils import send_otp_code
from .models import OtpCode
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, OtpCodeSerializer
from rest_framework.response import Response
from rest_framework import status


class UserRegisterView(APIView):
    """
        Method: POST
            Use for user registration
        inputs:
            - phone_number: 11 digits
            - email: at least 6 chars. max 255 chars
            - full_name: max 255 chars
            - password: at least 6 chars
            - password2: at least 6 chars. must be exact password

        return:
            - success: True if user created successfully (201), then should be redirected to verify url. Otherwise return errors list (400).

    """
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(ser_data.validated_data['phone_number'], random_code)
            ser_OtpCode = OtpCodeSerializer(data={'code': random_code,
                                                  'phone_number': ser_data.validated_data['phone_number']})
            if ser_OtpCode.is_valid():
                ser_OtpCode.save()
            request.session['user_registration_info'] = {
                # 'ser_data': ser_data,
                'phone_number': ser_data.validated_data['phone_number'],
                'email': ser_data.validated_data['email'],
                'full_name': ser_data.validated_data['full_name'],
                'password': ser_data.validated_data['password'],
                'password2': ser_data.validated_data['password2'],
            }
            # ser_data.create(ser_data.validated_data)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterVerifyCodeView(APIView):
    """
        Method: POST
            Use for confirm otp code
        input:
            - code: inserted otp code form user. 4 digits
        return:
            - success: True if user created successfully (201). Otherwise False (400).

    """
    def post(self, request, *args, **kwargs):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = OtpCodeSerializer(data=request.POST, partial=True)
        if form.is_valid():
            cd = form.validated_data
            if cd['code'] == code_instance.code:
                ser_user = UserRegisterSerializer(data=user_session, partial=True)
                print(ser_user)
                if ser_user.is_valid():
                    ser_user.create(ser_user.validated_data)
                    return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(LoginRequiredMixin, APIView):
    """
        Method: GET
            Use for user logout
            - User must be logged in before this.

        return:
            - success: True if user successfully logged out (200). Otherwise False (400).
    """
    def get(self, request, *args, **kwargs):
        if request.user:
            logout(request)
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
        Method: POST
            Use for user login
        input:
            - phone_number: 11 digits
            - password: at least 6 chars
        return:
            - success: True if user successfully logged in (200). Otherwise False(401).
    """
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user:
            login(request, user)
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)

