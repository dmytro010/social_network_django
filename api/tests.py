from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api import serializers
from .models import Post, User
from . import serializers
from django.urls import reverse
import json


class PostsApiTestCase(APITestCase):

    def setUp(self):
        self.post1 = Post.objects.create(title="test1", text="test1 text")
        self.post2 = Post.objects.create(title="test2", text="test2 text")
        self.valid_payload = {
            "title": "test1",
            "text": "test1 text"
            }
        self.invalid_payload = {
            "title": "",
            "text": "test1 text"
        }
        self.user = User.objects.create_superuser(username='testuser', password='test')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        
    def test_get_posts_list(self):
        # get API response
        response = self.client.get(reverse('posts-list'))
        # get data from db
        posts = Post.objects.all()
        serializer = serializers.PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_post(self):
        # get API response
        response = self.client.get(
            reverse('post-detail', kwargs={'pk': self.post1.pk}))
        # get data from db
        post = Post.objects.get(pk=self.post1.pk)
        serializer = serializers.PostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_invalid_single_post(self):
        response = self.client.get(
            reverse('post-detail', kwargs={'pk': 99}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_serializer(self):
        serializer_data = serializers.PostSerializer([self.post1, self.post2], many=True).data
        expected_data = [
            {
            "title": "test1",
            "text": "test1 text",
            "num_of_likes": 0
            },
            {
            "title": "test2",
            "text": "test2 text",
            "num_of_likes": 0
            }
        ]
        self.assertEqual(serializer_data, expected_data)

    def test_create_valid_post(self):

        response = self.client.post(
            reverse('posts-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_post(self):
        response = self.client.post(
            reverse('posts-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_post_unauthorized(self):
        self.client.logout()
        response = self.client.post(
            reverse('posts-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
