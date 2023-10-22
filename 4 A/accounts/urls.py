from django.urls import path
from . import views
# from rest_framework.authtoken import views as auth_token
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegister.as_view(), name="user_register"),
    # path('api-token-auth/', auth_token.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = routers.SimpleRouter()
router.register('user', views.UserViewSet)

urlpatterns += router.urls

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5ODA1ODUwNywiaWF0IjoxNjk3OTcyMTA3LCJqdGkiOiJhZDlkNzE3Yjc1NDE0OGVkOGI1NzMxMzNmY2U5YzNiNiIsInVzZXJfaWQiOjF9.e9UsoG8CrDhMMr511On4bKOw_EOmGEleE1W_F4F32tc",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3OTcyNDA3LCJpYXQiOjE2OTc5NzIxMDcsImp0aSI6ImUxODhkMjI4ZTBkMDRiZDI4YmQ4MTQwMzQ1N2NmYjcyIiwidXNlcl9pZCI6MX0.uydria4ui-bvVyIXtdSJ8Sl0bwPtSnB9CpkGivEkf3Q"