from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Post,Comment
from . import models
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [ 'id','content','image','created_at' ,'writer']

class CommentSerializer(ModelSerializer):
    
    class Meta:
        model = Comment
        fields = [ 'id','comment','writer','created_at','post' ]


class AlbumSerializer(ModelSerializer) :
    writer = serializers.ReadOnlyField(source = 'writer.username')
    class Meta :
        model = models.Album
        fields = ['image', 'created_at', 'writer', 'test']
        #fields = '__all__'

