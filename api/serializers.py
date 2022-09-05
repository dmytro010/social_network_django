from rest_framework import serializers
from .models import Post, User, PostLike

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "text", "num_of_likes")

class UserSerializer(serializers.ModelSerializer):
    get_last_login = serializers.DateTimeField()
    get_posts_liked = PostSerializer(source='posts_liked', many=True)
    get_posts_created = PostSerializer(source='posts_created', many=True)

    class Meta:
        model = User
        fields = ("username", "last_request", "get_last_login", "get_posts_liked", "get_posts_created")

class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ("__all__" )

# class NumLikeSerializer(serializers.ModelSerializer):
#     num_likes = serializers.DateTimeField()
#     class Meta:
#         model = Post
#         fields = ("post", "date", "user" )
    
# class TotalLikeSerializer(serializers.ModelSerializer):
#     total_likes = serializers.IntegerField()
#     total_num = serializers.SerializerMethodField()
#     class Meta:
#         model = PostLike
#         fields = '__all__'

#     def get_total_num(self, obj):
#         return PostLike.objects.count()



