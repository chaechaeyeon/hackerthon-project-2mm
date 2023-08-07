from rest_framework import serializers
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()

class PhoneNumberSerializer(serializers.Serializer):
    phone = PhoneNumberField()

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
