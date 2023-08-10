from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from . import models

class AlbumSerializer(ModelSerializer) :
    writer = serializers.ReadOnlyField(source = 'writer.username')
    class Meta :
        model = models.Album
        fields = ['image', 'created_at', 'writer', 'test']
        #fields = '__all__'