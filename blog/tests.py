from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Comment, Post


class PostAPITestCase(APITestCase):
    """Test cases for Post endpoints."""

    def setUp(self):
        """Set up test data."""
        self.post_data = {
            "title": "Test Post",
            "content": "This is a test post content.",
            "author": "John Doe",
        }
        self.post = Post.objects.create(**self.post_data)

    def test_create_post(self):
        """Test creating a new post via POST /api/posts/."""
        url = reverse("post-list")
        data = {
            "title": "New Post",
            "content": "Content of new post",
            "author": "Jane Doe",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["content"], data["content"])
        self.assertEqual(response.data["author"], data["author"])
        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_create_post_missing_fields(self):
        """Test creating a post with missing required fields."""
        url = reverse("post-list")
        data = {"title": "Incomplete Post"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)
        self.assertIn("author", response.data)

    def test_list_posts(self):
        """Test listing all posts via GET /api/posts/."""
        # Create additional posts
        Post.objects.create(title="Second Post", content="Content 2", author="Jane Doe")
        Post.objects.create(title="Third Post", content="Content 3", author="Bob Smith")

        url = reverse("post-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)
        # Check that list serializer is used (no created_at/updated_at in list view)
        self.assertIn("id", response.data["results"][0])
        self.assertIn("title", response.data["results"][0])
        self.assertIn("content", response.data["results"][0])
        self.assertIn("author", response.data["results"][0])
        # List serializer should not include created_at/updated_at
        self.assertNotIn("created_at", response.data["results"][0])
        self.assertNotIn("updated_at", response.data["results"][0])

    def test_list_posts_pagination(self):
        """Test that post listing supports pagination."""
        # Create more than PAGE_SIZE posts (PAGE_SIZE is 10)
        for i in range(15):
            Post.objects.create(
                title=f"Post {i}",
                content=f"Content {i}",
                author=f"Author {i}",
            )

        url = reverse("post-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertEqual(len(response.data["results"]), 10)  # PAGE_SIZE
        self.assertEqual(response.data["count"], 16)  # 15 new + 1 from setUp

    def test_get_post_detail(self):
        """Test retrieving a specific post via GET /api/posts/{id}/."""
        url = reverse("post-detail", kwargs={"pk": self.post.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.post.id)
        self.assertEqual(response.data["title"], self.post.title)
        self.assertEqual(response.data["content"], self.post.content)
        self.assertEqual(response.data["author"], self.post.author)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_get_post_detail_not_found(self):
        """Test retrieving a non-existent post returns 404."""
        url = reverse("post-detail", kwargs={"pk": 99999})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post(self):
        """Test updating a post via PUT /api/posts/{id}/."""
        url = reverse("post-detail", kwargs={"pk": self.post.pk})
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "author": "Updated Author",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, updated_data["title"])
        self.assertEqual(self.post.content, updated_data["content"])
        self.assertEqual(self.post.author, updated_data["author"])

    def test_update_post_partial(self):
        """Test partial update of a post via PATCH /api/posts/{id}/."""
        url = reverse("post-detail", kwargs={"pk": self.post.pk})
        updated_data = {"title": "Partially Updated Title"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, updated_data["title"])
        # Other fields should remain unchanged
        self.assertEqual(self.post.content, self.post_data["content"])
        self.assertEqual(self.post.author, self.post_data["author"])

    def test_delete_post(self):
        """Test deleting a post via DELETE /api/posts/{id}/."""
        url = reverse("post-detail", kwargs={"pk": self.post.pk})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_delete_post_not_found(self):
        """Test deleting a non-existent post returns 404."""
        url = reverse("post-detail", kwargs={"pk": 99999})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentAPITestCase(APITestCase):
    """Test cases for Comment endpoints."""

    def setUp(self):
        """Set up test data."""
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content",
            author="John Doe",
        )
        self.comment_data = {
            "content": "This is a test comment.",
            "author": "Jane Doe",
        }
        self.comment = Comment.objects.create(post=self.post, **self.comment_data)

    def test_create_comment(self):
        """Test creating a new comment via POST /api/posts/{id}/comments/."""
        url = reverse("post-comments", kwargs={"pk": self.post.pk})
        data = {
            "content": "New comment content",
            "author": "Bob Smith",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(response.data["content"], data["content"])
        self.assertEqual(response.data["author"], data["author"])
        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        # Verify the comment is associated with the correct post
        comment = Comment.objects.get(pk=response.data["id"])
        self.assertEqual(comment.post, self.post)

    def test_create_comment_missing_fields(self):
        """Test creating a comment with missing required fields."""
        url = reverse("post-comments", kwargs={"pk": self.post.pk})
        data = {"content": "Incomplete comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("author", response.data)

    def test_create_comment_post_not_found(self):
        """Test creating a comment for a non-existent post returns 404."""
        url = reverse("post-comments", kwargs={"pk": 99999})
        data = {"content": "Comment", "author": "Author"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_comments(self):
        """Test listing comments for a post via GET /api/posts/{id}/comments/."""
        # Create additional comments
        Comment.objects.create(post=self.post, content="Second comment", author="Bob Smith")
        Comment.objects.create(post=self.post, content="Third comment", author="Alice Johnson")

        # Create a comment for a different post (should not appear)
        other_post = Post.objects.create(title="Other Post", content="Other content", author="Other Author")
        Comment.objects.create(post=other_post, content="Other post comment", author="Someone")

        url = reverse("post-comments", kwargs={"pk": self.post.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Only comments for self.post
        # Verify all comments belong to the correct post
        for comment_data in response.data:
            comment = Comment.objects.get(pk=comment_data["id"])
            self.assertEqual(comment.post, self.post)

    def test_list_comments_empty(self):
        """Test listing comments for a post with no comments."""
        new_post = Post.objects.create(title="New Post", content="Content", author="Author")
        url = reverse("post-comments", kwargs={"pk": new_post.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])

    def test_get_comment_detail(self):
        """Test retrieving a specific comment via GET /api/posts/{id}/comments/{id}/."""
        url = reverse(
            "post-comment-detail",
            kwargs={"pk": self.post.pk, "comment_id": self.comment.pk},
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.comment.id)
        self.assertEqual(response.data["content"], self.comment.content)
        self.assertEqual(response.data["author"], self.comment.author)
        self.assertIn("created_at", response.data)

    def test_get_comment_detail_not_found(self):
        """Test retrieving a non-existent comment returns 404."""
        url = reverse(
            "post-comment-detail",
            kwargs={"pk": self.post.pk, "comment_id": 99999},
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_detail_wrong_post(self):
        """Test retrieving a comment that belongs to a different post returns 404."""
        other_post = Post.objects.create(title="Other Post", content="Content", author="Author")
        url = reverse(
            "post-comment-detail",
            kwargs={"pk": other_post.pk, "comment_id": self.comment.pk},
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment(self):
        """Test deleting a comment via DELETE /api/posts/{id}/comments/{id}/."""
        url = reverse(
            "post-comment-detail",
            kwargs={"pk": self.post.pk, "comment_id": self.comment.pk},
        )
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_not_found(self):
        """Test deleting a non-existent comment returns 404."""
        url = reverse(
            "post-comment-detail",
            kwargs={"pk": self.post.pk, "comment_id": 99999},
        )
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_wrong_post(self):
        """Test deleting a comment that belongs to a different post returns 404."""
        other_post = Post.objects.create(title="Other Post", content="Content", author="Author")
        url = reverse(
            "post-comment-detail",
            kwargs={"pk": other_post.pk, "comment_id": self.comment.pk},
        )
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
