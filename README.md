# Django Blog API

A RESTful API for a blogging platform built with Django and Django REST Framework. This API allows users to interact with blog posts and comments through a comprehensive set of endpoints.

## Features

- **Blog Posts Management**: Full CRUD operations for blog posts
- **Comments System**: Create, read, and delete comments on posts
- **RESTful Design**: Well-structured API following REST principles
- **No Authentication Required**: Open API for easy interaction
- **Comprehensive Testing**: Unit tests covering critical functionality

## Technologies Used

- Python 3.13+
- Django 6.0+
- Django REST Framework 3.16.1+
- uv (for dependency management)

## Project Setup

### Prerequisites

- Python 3.13 or higher
- uv (Python package manager)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd django-blog
   ```

2. **Set up virtual environment and install dependencies**

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional, for admin access)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Blog Posts

#### Create a Post

- **POST** `/api/posts/`
- **Request Body:**

  ```json
  {
    "title": "My First Post",
    "content": "This is the content of my blog post.",
    "author": "John Doe"
  }
  ```

- **Response:** 201 Created with the created post object

#### List All Posts

- **GET** `/api/posts/`
- **Response:** List of all posts with fields: `id`, `title`, `content`, `author`
- **Note:** Supports pagination

#### Get Post Details

- **GET** `/api/posts/{id}/`
- **Response:** Post details including `title`, `content`, `created_at`, `updated_at`, `author`

#### Update a Post

- **PUT** `/api/posts/{id}/`
- **Request Body:**

  ```json
  {
    "title": "Updated Title",
    "content": "Updated content",
    "author": "John Doe"
  }
  ```

- **Note:** Any user can update any post (no author restrictions)

#### Delete a Post

- **DELETE** `/api/posts/{id}/`
- **Response:** 204 No Content
- **Note:** Any user can delete any post

### Comments

#### Create a Comment

- **POST** `/api/posts/{post_id}/comments/`
- **Request Body:**

  ```json
  {
    "content": "This is a comment on the post.",
    "author": "Jane Doe"
  }
  ```

- **Response:** 201 Created with the created comment object

#### List Comments for a Post

- **GET** `/api/posts/{post_id}/comments/`
- **Response:** List of comments with fields: `id`, `content`, `author`, `created_at`

#### Get Comment Details

- **GET** `/api/posts/{post_id}/comments/{id}/`
- **Response:** Comment details including `content`, `author`, `created_at`

#### Delete a Comment

- **DELETE** `/api/posts/{post_id}/comments/{id}/`
- **Response:** 204 No Content
- **Note:** Any user can delete any comment

## Models

### Post Model

- `title` (CharField)
- `content` (TextField)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)
- `author` (CharField)

### Comment Model

- `content` (TextField)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)
- `post` (ForeignKey to Post)
- `author` (CharField)

## Testing

Run the test suite using:

```bash
python manage.py test
```

The test suite covers:

- Creating posts via API
- Listing posts
- Creating comments
- Permissions (ensuring users can update/delete any post/comment)
- Pagination functionality

## Project Structure

```bash
django-blog/
├── manage.py
├── pyproject.toml
├── README.md
└── <project_name>/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
└── <app_name>/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── tests.py
```

## API Usage Examples

### Using cURL

**Create a post:**

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "Post content", "author": "John Doe"}'
```

**Get all posts:**

```bash
curl http://127.0.0.1:8000/api/posts/
```

**Create a comment:**

```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/comments/ \
  -H "Content-Type: application/json" \
  -d '{"content": "Great post!", "author": "Jane Doe"}'
```

### Using Python requests

```python
import requests

# Create a post
response = requests.post('http://127.0.0.1:8000/api/posts/', json={
    'title': 'My Post',
    'content': 'Post content',
    'author': 'John Doe'
})
print(response.json())

# Get all posts
response = requests.get('http://127.0.0.1:8000/api/posts/')
print(response.json())
```

## Development

### Running Migrations

After making model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Django Admin

If you created a superuser, access the admin panel at:
`http://127.0.0.1:8000/admin/`

## Evaluation Criteria

This project demonstrates:

- ✅ **API Design**: RESTful principles and well-structured endpoints
- ✅ **Django REST Framework**: Effective use of serializers and views
- ✅ **Testing**: Comprehensive unit tests covering critical functionality
- ✅ **Clean Code**: Well-organized, readable, and maintainable codebase

## License

This project is part of a coding challenge.

## Contributing

This is a challenge project. For questions or issues, please refer to the challenge documentation.