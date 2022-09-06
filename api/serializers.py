from rest_framework import serializers
from .models import Post, User, PostLike

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "text", "num_of_likes")

class UserSerializer(serializers.ModelSerializer):
    get_last_login = serializers.DateTimeField()
    get_posts_liked = PostSerializer(source='posts_liked', many=True)

    class Meta:
        model = User
        fields = ("username", "last_request", "get_last_login", "get_posts_liked")

class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ("__all__" )