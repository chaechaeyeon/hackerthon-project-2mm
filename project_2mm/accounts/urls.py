from django.urls import path
from .views import UsernameView, PhoneNumberView, PasswordView

urlpatterns = [
    path('username/', UsernameView.as_view(), name='username-view'),
    path('phonenumber/', PhoneNumberView.as_view(), name='phone-number-view'),
    path('password/', PasswordView.as_view(), name='password-view'),
]
