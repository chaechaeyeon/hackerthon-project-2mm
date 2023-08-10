from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [ 'id','content','image','created_at' ,'writer']

# class CommentSerializer(ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = [ 'comment', 'post' ]