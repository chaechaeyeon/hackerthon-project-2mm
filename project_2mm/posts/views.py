from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.permissions import  IsAuthenticated
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
   
    
    def create(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            writer = request.user #request.user를 writer로 받아오기 
            serializer.save(writer=writer)
            headers = self.get_success_headers(serializer.data) #성공시 헤더로 전달할 값들을 headers에 담기
            return Response(serializer.data,headers=headers)
        else:
            print("이거 뜨면 세션값 못 받고 있는거임 수정해야함.ㅜㅜ")
            return Response(serializer.data,{'error'}, status=status.HTTP_401_UNAUTHORIZED)