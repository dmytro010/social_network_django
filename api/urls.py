from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('posts/', views.PostList.as_view(), name='posts-list' ),  
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail' ),
    path('posts/<int:pk>/like/', views.post_like, name='like'),
    path('posts/<int:pk>/unlike/', views.post_unlike, name='unlike'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('analytics/', views.analytics, name="analytics")
]