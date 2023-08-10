from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views

urlpatterns = [
    path('album/', views.AlbumAPIView.as_view(), name='album-list'), # 업로드 된 사진 전체
]
