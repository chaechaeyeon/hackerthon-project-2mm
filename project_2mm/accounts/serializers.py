from rest_framework import serializers
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField
from posts import models

class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()
    class Meta:
        model = models.User
        fields = '__all__'
    def update(self, instance, validated_data):
        # 코드 값을 무시하고 업데이트할 필드만 validated_data에서 추출합니다.
        validated_data.pop('user', None)
        return super().update(instance, validated_data)

# class PhoneNumberSerializer(serializers.Serializer):
#     phone = PhoneNumberField

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

class UsersSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    phone = PhoneNumberField


# 모임코드생성 
class GroupSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = models.Group
        fields = ['name','info', 'profile', 'username', 'code']
    def update(self, instance, validated_data):
        # 코드 값을 무시하고 업데이트할 필드만 validated_data에서 추출합니다.
        validated_data.pop('code', None)
        return super().update(instance, validated_data)