from rest_framework import serializers
from .models import CatProfile, Post

class CatProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatProfile
        fields = '__all__' # Esto enviará todos los campos (nombre, bio, etc.)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'