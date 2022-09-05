from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import PostSerializer, UserSerializer
from .models import Post, User, PostLike
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def index(request):
    title = "Welcome to social network"
    return render(request, 'index.html', {"title": title})

"""API VIEWS"""

"""Post list view.
    includes all posts """
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)


"""Post datail view """
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

"""Post like view"""
@api_view()
@permission_classes([permissions.IsAuthenticated])
def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
        
    if post.likes.filter(id= request.user.id).exists():
        
        return Response({"message": f"The post: {post} already has like. You can't add more than one like."})

    else:
        post.likes.add(request.user)
        post.save()
        return Response({"message": f"The post: {post} was liked successfuly"})

"""Post unlike view"""
@api_view()
@permission_classes([permissions.IsAuthenticated])
def post_unlike(request, pk):
    post = get_object_or_404(Post, id=pk)
        
    if post.likes.filter(id= request.user.id).exists():
        post.likes.remove(request.user)
        post.save()
        return Response({"message": f"The post: {post} was unliked successfuly"})

    else:
        return Response({"message": f"The post: {post} can't be unliked, you have not liked the post yet."})
 

    # return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

"""User detail view.
    includes last_request and last_login info """
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('post_liked')
    permission_classes = (permissions.IsAuthenticated,)

"""Analytics view
   total likes filtered by date."""
@api_view()
@permission_classes([permissions.IsAuthenticated])
def analytics(request):
  
    date_from = request.query_params.get("date_from")
    date_to = request.query_params.get("date_to")
    #if user enters date_from and date_to params, we filter data by params
    if date_from and date_to:
        data = PostLike.objects.filter(date__gte=date_from, date__lte=date_to).count()
    #if no params, we return num of likes for whole period
    else:
        data = PostLike.objects.count()

    return Response({"num of likes": data})



