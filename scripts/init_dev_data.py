#!/usr/bin/env python
"""
Initialize development environment with dummy data for all models.

How to run:
python -m scripts.init_dev_data
"""

import os
import sys

from django.contrib.auth import get_user_model

from blog.models import Comment, Post

User = get_user_model()


def create_superuser():
    """Create a superuser for development."""
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' already exists")
        return

    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")


def create_dummy_posts():
    """Create dummy blog posts."""
    posts_data = [
        {
            "title": "Getting Started with Django",
            "content": """Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

            In this post, we'll explore the basics of Django and how to set up your first project. Django follows the MVT (Model-View-Template) architectural pattern, which is similar to MVC but adapted for Django's philosophy.

            Key features of Django include:
            - An object-relational mapper (ORM) for database interactions
            - A powerful admin interface
            - Built-in authentication and authorization
            - URL routing and view system
            - Template engine for rendering HTML

            Let's dive in and start building amazing web applications!""",
            "author": "Jane Developer",
        },
        {
            "title": "Understanding Django REST Framework",
            "content": """Django REST Framework (DRF) is a powerful and flexible toolkit for building Web APIs in Django. It provides serializers, viewsets, and authentication mechanisms that make it easy to create RESTful APIs.

            One of the key advantages of DRF is its browsable API feature, which allows developers to interact with the API directly from the browser. This makes testing and debugging much easier during development.

            DRF includes:
            - Serializers for converting complex data types to Python native types
            - ViewSets and Generic Views for handling common API patterns
            - Authentication and permissions classes
            - Throttling for rate limiting
            - Pagination support
            - Filtering and search capabilities

            Whether you're building a simple API or a complex microservices architecture, DRF has the tools you need.""",
            "author": "John Coder",
        },
        {
            "title": "Best Practices for Django Models",
            "content": """Django models are the single, definitive source of information about your data. They contain the essential fields and behaviors of the data you're storing. Following best practices when designing your models can save you a lot of headaches later.

            Here are some key best practices:

            1. **Use descriptive field names**: Choose names that clearly indicate what the field represents.

            2. **Add help text**: Use the `help_text` parameter to document what each field is for.

            3. **Set appropriate max_length**: Don't use unnecessarily large max_length values, but also don't make them too restrictive.

            4. **Use ForeignKey for relationships**: When you have a relationship between models, use ForeignKey, ManyToManyField, or OneToOneField appropriately.

            5. **Add Meta options**: Use Meta class to add ordering, verbose names, and other model-level options.

            6. **Override __str__ method**: This makes your models more readable in the Django admin and shell.

            7. **Use migrations**: Always use migrations to track changes to your models. Never edit migrations manually unless absolutely necessary.

            Following these practices will make your Django application more maintainable and easier to work with.""",
            "author": "Sarah Tech",
        },
        {
            "title": "Django Testing Strategies",
            "content": """Testing is a crucial part of software development, and Django provides excellent tools for writing and running tests. The Django test framework is built on Python's unittest module, but adds Django-specific features.

            Django's test framework includes:
            - TestCase class with database transaction rollback
            - Client for simulating HTTP requests
            - Test fixtures and factories
            - Coverage tools integration

            When writing tests for Django applications, consider:
            - Unit tests for individual functions and methods
            - Integration tests for views and API endpoints
            - Model tests for custom model methods
            - Form validation tests
            - Template rendering tests

            Remember: good tests are fast, isolated, repeatable, and self-validating. They should clearly express what they're testing and why.""",
            "author": "Mike Tester",
        },
        {
            "title": "Deploying Django Applications",
            "content": """Deploying a Django application to production requires careful planning and consideration of several factors. From choosing the right hosting platform to configuring your database and static files, there's a lot to think about.

            Key considerations for deployment:
            - **Environment variables**: Use environment variables for sensitive settings like SECRET_KEY and database credentials
            - **Static files**: Configure STATIC_ROOT and use a service like WhiteNoise or a CDN
            - **Database**: Choose an appropriate database (PostgreSQL is recommended for production)
            - **WSGI server**: Use Gunicorn or uWSGI instead of Django's development server
            - **Reverse proxy**: Use Nginx or Apache as a reverse proxy
            - **Security**: Enable HTTPS, set DEBUG=False, configure ALLOWED_HOSTS
            - **Monitoring**: Set up error tracking and logging
            - **Backups**: Implement regular database backups

            Popular deployment platforms include:
            - Heroku
            - AWS (Elastic Beanstalk, EC2, etc.)
            - DigitalOcean
            - Railway
            - Render

            Each platform has its own advantages, so choose based on your specific needs and budget.""",
            "author": "Alex DevOps",
        },
    ]

    created_posts = []
    for post_data in posts_data:
        post, created = Post.objects.get_or_create(
            title=post_data["title"],
            defaults={
                "content": post_data["content"],
                "author": post_data["author"],
            },
        )
        if created:
            print(f"Created post: {post.title}")
        else:
            print(f"Post already exists: {post.title}")
        created_posts.append(post)

    return created_posts


def create_dummy_comments(posts):
    """Create dummy comments for blog posts."""
    comments_data = [
        {
            "post_index": 0,
            "content": "Great introduction! I'm new to Django and this was very helpful.",
            "author": "Beginner Dev",
        },
        {
            "post_index": 0,
            "content": "Thanks for sharing. Can you provide more examples of the ORM usage?",
            "author": "Curious Coder",
        },
        {
            "post_index": 1,
            "content": "DRF is amazing! The browsable API feature is a game-changer for development.",
            "author": "API Enthusiast",
        },
        {
            "post_index": 1,
            "content": "I've been using DRF for a year now. The serializers are incredibly powerful.",
            "author": "Experienced Dev",
        },
        {
            "post_index": 2,
            "content": "These best practices are spot on. I wish I knew these when I started!",
            "author": "Learning Dev",
        },
        {
            "post_index": 2,
            "content": "Don't forget about using `db_index=True` for frequently queried fields!",
            "author": "Performance Guru",
        },
        {
            "post_index": 3,
            "content": "Testing is so important. Thanks for emphasizing this!",
            "author": "Quality Advocate",
        },
        {
            "post_index": 3,
            "content": "I use pytest-django for testing. It's a great alternative to Django's test framework.",
            "author": "Pytest Fan",
        },
        {
            "post_index": 4,
            "content": "Deployment can be tricky. This guide covers all the important points!",
            "author": "Deployment Newbie",
        },
        {
            "post_index": 4,
            "content": "I've had good experience with Railway. It's simple and works well for Django apps.",
            "author": "Railway User",
        },
        {
            "post_index": 4,
            "content": "Don't forget to set up monitoring and error tracking (Sentry is great for this)!",
            "author": "Ops Expert",
        },
    ]

    created_count = 0
    for comment_data in comments_data:
        post = posts[comment_data["post_index"]]
        comment, created = Comment.objects.get_or_create(
            post=post,
            content=comment_data["content"],
            author=comment_data["author"],
        )
        if created:
            created_count += 1
            print(f"Created comment by {comment.author} on '{post.title}'")

    return created_count


def main():
    """Main function to initialize development data."""
    print("Initializing development data...")
    print("-" * 50)

    # Create superuser
    print("\nCreating superuser...")
    create_superuser()

    # Create posts
    print("\nCreating blog posts...")
    posts = create_dummy_posts()

    # Create comments
    print("\nCreating comments...")
    create_dummy_comments(posts)

    # Summary
    print("\n" + "-" * 50)
    print("Summary:")
    print(f"  Superusers: {User.objects.filter(is_superuser=True).count()}")
    print(f"  Posts: {Post.objects.count()}")
    print(f"  Comments: {Comment.objects.count()}")
    print("\nDevelopment data initialization complete!")


if __name__ == "__main__":
    main()
