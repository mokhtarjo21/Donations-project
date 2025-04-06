from rest_framework import serializers
from .models import Comment
from django.contrib.auth.models import User
from .models import Project

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'project', 'content', 'created_at', 'parent']
        read_only_fields = ['created_at']