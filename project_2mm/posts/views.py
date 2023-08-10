from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import views
from rest_framework.response import Response
from . import models
from . import serializers
# Create your views here.

# 사진 리스트 
class AlbumAPIView(views.APIView):
    def get(self, request):
        serializer = serializers.AlbumSerializer(models.Album.objects.all(), many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = serializers.AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400) 
    # 로그인 완료 되면 확인하기 
    # def delete(self, request, pk):
    #     album = models.Album.objects.get(pk=pk)
    #     if album is not None :
    #         if album.writer == request.user :
    #             album.delete()