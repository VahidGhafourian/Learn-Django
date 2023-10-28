from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
import random
from utils import send_otp_code
from .models import OtpCode
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, OtpCodeSerializer
from rest_framework.response import Response
from rest_framework import status


class UserRegisterView(APIView):
    # form_class = UserRegistrationForm
    # template_name = 'accounts/register.html'

    # def get(self, request):
    #     form = self.form_class
    #     return render(request, self.template_name, {'form': form})

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
            return Response({'message': 'Code Sent'}, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     random_code = random.randint(1000, 9999)
        #     send_otp_code(form.cleaned_data['phone'], random_code)
        #     OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
        #     request.session['user_registration_info'] = {
        #         'phone_number': form.cleaned_data['phone'],
        #         'email': form.cleaned_data['email'],
        #         'full_name': form.cleaned_data['full_name'],
        #         'password': form.cleaned_data['password'],
        #     }
        #     messages.success(request, 'we sent you a code', 'success')
        #     return redirect('accounts:verify_code')
        # return render(request, self.template_name, {'form': form})

class UserRegisterVerifyCodeView(APIView):
    # form_class = VerifyCodeForm
    # def get(self, request):
    #     form = self.form_class
    #     return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
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
                    return Response({'message': 'User Created'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Wrong Code'}, status=status.HTTP_400_BAD_REQUEST)
        #         messages.success(request, 'you registered', 'success')
        #         return redirect('home:home')
        #     else:
        #         messages.error(request, 'this code is wrong', 'danger')
        #         return redirect('accounts:verify_code')
        # return redirect('home:home')


class UserLogoutView(LoginRequiredMixin, APIView):
    def get(self, request):
        logout(request)
        # messages.success(request, 'you logged out successfully', 'success')
        # return redirect('home:home')
        return Response({'message': 'success'})

class UserLoginView(APIView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        if not request.user.is_anonymous:
            return redirect('home:home')
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'phone number or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})
