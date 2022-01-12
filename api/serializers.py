from rest_framework import serializers
from .models.blog import Blog
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password')

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'image', 'title', 'author', 'content',
                  'updated_at', 'created_at')

    def get_author(self, obj):
        return obj.author.email
