from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UsernameSerializer, PasswordSerializer, PhoneNumberSerializer
from phonenumber_field.modelfields import PhoneNumber
from posts.models import UserInfo

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