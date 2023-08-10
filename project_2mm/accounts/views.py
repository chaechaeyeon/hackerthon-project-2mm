from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import viewsets, generics
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import UsernameSerializer, PasswordSerializer, PhoneNumberSerializer
from . import serializers
from phonenumber_field.modelfields import PhoneNumber
from posts.models import UserInfo
from posts import models
from rest_framework.decorators import action
from rest_framework.decorators import api_view
import uuid

class UsernameView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsernameSerializer(data=request.data)
        if serializer.is_valid():
            self.request.session['username'] = serializer.validated_data['username']
            #디버그 확인
            print("Debug :username:", serializer.validated_data.get('username'))
            print("Debug : Username Session:", self.request.session.get('username'))
            return Response({'next_url': 'phonenumber/'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhoneNumberView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number_str = serializer.validated_data.get('phone')
            e164_phone_number = PhoneNumber.from_string(phone_number_str)
            
            self.request.session['phone'] = str(e164_phone_number)
            #디버그 확인 
            print("Debug : Phone Number:", serializer.validated_data.get('phone'))
            print("Debug :phone Session:", self.request.session.get('phone'))
            return Response({'next_url': 'password/'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = self.request.session.get('username')
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data.get('password')

            if not username or not phone:
                return Response({'error': '정보 누락'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.create_user(username=username, password=password)
                user.userinfo.phone.as_e164= phone
                user.save()
            except Exception as e:
                return Response({'error': '회원 가입 오류.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': '회원 가입 성공'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# group 개별 코드 발급 위한 viewset
class GroupListCreateView(generics.ListCreateAPIView):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer 

# group 정보 부분 수정위한 viewset
class GroupDetailView(APIView):
    def get_object(self, code):
        try:
            return models.Group.objects.get(code=code)
        except models.Group.DoesNotExist:
            return None

    def get(self, request, code):
        queryset = self.get_object(code)
        if queryset is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.GroupSerializer(queryset)
        return Response(serializer.data)
    def put(self, request, code):
        queryset = self.get_object(code)
        if queryset is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.GroupSerializer(queryset, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, code, format=None):
        try:
            queryset = models.Group.objects.get(code=code)
            serializer = serializers.GroupSerializer(queryset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Group.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)