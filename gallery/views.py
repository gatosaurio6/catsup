from rest_framework import viewsets
from .models import CatProfile, Post
from .serializers import CatProfileSerializer, PostSerializer

class CatProfileViewSet(viewsets.ModelViewSet):
    queryset = CatProfile.objects.all()
    serializer_class = CatProfileSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer