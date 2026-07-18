from rest_framework import serializers
from .models import CatProfile, Post, Comment

class CatProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatProfile
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'cat', 'image', 'caption', 'likes', 'created_at', 'comments']