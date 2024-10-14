import uuid
from rest_framework import serializers
from django.db import models
from post.models import Post, Comment
from account.models import User

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'parent', 'is_deleted', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']