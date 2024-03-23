from django.db.models import fields
from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk", "userId", "title", "body")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("pk", "postId", "name", "email", "body")
