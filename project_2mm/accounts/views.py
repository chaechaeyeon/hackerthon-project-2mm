from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login , logout


from .serializers import UsernameSerializer, PasswordSerializer
from . import serializers
from phonenumber_field.modelfields import PhoneNumber
from posts.models import UserInfo
from posts import models
from rest_framework.decorators import action
from rest_framework.decorators import api_view
import uuid


User = get_user_model()

#로그인 
class Loginview(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')
        try:
            user_info = UserInfo.objects.get(phone=phone)
            user = authenticate(request, username=user_info.user, password=password)

            if user is not None:
                login(request, user)
                #토큰 생성 
                token, created = Token.objects.get_or_create(user=user)
                
                # 디버그 확인용 : 로그인 유저 
                if request.user.is_authenticated:
                    print(request.user, "님이 로그인되었습니다:", token.key)
                else:
                    print("현재 로그인되어 있지 않습니다.")

                return Response({ 'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '로그인실패! 다시 시도'}, status=status.HTTP_401_UNAUTHORIZED)
        except UserInfo.DoesNotExist:
            return Response({'error': 'userinfo가 비어있음!'}, status=status.HTTP_404_NOT_FOUND)
 
#로그아웃 
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        #디버그 확인 :로그아웃
        if user.is_authenticated:
            print(user,"님이 로그아웃:" )
        else:
            print("현재 로그인되어 있지 않습니다.")
        return Response({'message': '로그아웃'}, status=status.HTTP_200_OK)
    
#회원가입 절차 
#STEP 1: username
class UsernameView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsernameSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            self.request.session['username'] = username
            #디버그 확인: 유저이름
            print("Debug :username:", serializer.validated_data.get('username'))
            print("Debug : Username Session:", self.request.session.get('username'))
            return Response({'next_url': 'phonenumber/'})
        else: 
            return Response({'넘어가는 거 막기..'},status=status.HTPP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#STEP2 : phonenumber
class PhoneNumberView(APIView):
    def post(self, request, *args, **kwargs):
        
        phone = request.data.get('phone') 

        if not phone:
            return Response({'error': '전화번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        # 세션에  저장
        self.request.session['phone'] = phone
        saved_phone = self.request.session.get('phone')
        
        print("Saved Phone Number in Session:", saved_phone)
        return Response({'next_url': 'password/'})
    

#STEP3: password
class PasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = self.request.session.get('username')
            phone = self.request.session.get('phone')  

            if not username or not phone:

                return Response({'error': '정보 누락'}, status=status.HTTP_400_BAD_REQUEST)

            password = serializer.validated_data.get('password')
            try:
                # 유저 생성 및 저장
                user = User.objects.create_user(username=username, password=password)
                user_info = UserInfo.objects.create(user=user, phone=phone)
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