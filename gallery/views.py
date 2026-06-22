from rest_framework import viewsets
from .models import CatProfile, Post, Comment 
from .serializers import CatProfileSerializer, PostSerializer, CommentSerializer 
class CatProfileViewSet(viewsets.ModelViewSet):
    queryset = CatProfile.objects.all()
    serializer_class = CatProfileSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer