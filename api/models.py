
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    last_request = models.DateTimeField(blank=True, null=True)

    @property
    def get_last_login(self):
        return self.last_login
    
    @property
    def get_posts_liked(self):
        return self.posts_liked
    
    # @property
    # def get_posts_created(self):
    #     return self.posts_created
    
    
    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PostLike', related_name='posts_liked')
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts_created")
    

    @property
    def num_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    @classmethod
    def total_likes(cls):
        return cls.objects.count()

    def __str__(self):
        return self.user.username, self.post.title, self.date.strftime("%Y-%m-%d %I:%M")

