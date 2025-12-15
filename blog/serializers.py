from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for listing posts (without full content)."""

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author"]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    class Meta:
        model = Comment
        fields = ["id", "content", "author", "created_at"]
        read_only_fields = ["id", "created_at"]
