from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet

post_router = DefaultRouter()
post_router.register('posts', PostViewSet,basename='post')


urlpatterns = [
     path('', include(post_router.urls)),
]
