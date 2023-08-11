from rest_framework.routers import SimpleRouter, DefaultRouter
from django.urls import path, include
from .views import PostViewSet,CommentViewSet
from . import views
post_router = DefaultRouter()
post_router.register('posts', PostViewSet,basename='post')

comment_router = DefaultRouter()
comment_router.register('comments',CommentViewSet,basename='comment')

urlpatterns = [
    path('', include(post_router.urls)),
    path('posts/<int:post_id>/',include(comment_router.urls)),
    
    path('album/', views.AlbumAPIView.as_view(), name='album-list'), # 업로드 된 사진 전체
    

]
