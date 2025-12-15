from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment, Post
from .serializers import CommentSerializer, PostListSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Post instances.
    Provides list, create, retrieve, update, and delete operations.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        """Use PostListSerializer for list action, PostSerializer for others."""
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        """
        List comments for a post or create a new comment.
        GET /api/posts/{id}/comments/ - List all comments for the post
        POST /api/posts/{id}/comments/ - Create a new comment
        """
        post = self.get_object()

        if request.method == "GET":
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["get", "delete"],
        url_path="comments/(?P<comment_id>[^/.]+)",
        url_name="comment-detail",
    )
    def comment_detail(self, request, pk=None, comment_id=None):
        """
        Retrieve or delete a specific comment.
        GET /api/posts/{id}/comments/{comment_id}/ - Get comment details
        DELETE /api/posts/{id}/comments/{comment_id}/ - Delete comment
        """
        post = self.get_object()
        comment = get_object_or_404(Comment, pk=comment_id, post=post)

        if request.method == "GET":
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        if request.method == "DELETE":
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
