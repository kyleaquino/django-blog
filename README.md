# Django Blog API

A RESTful API for a blogging platform built with Django and Django REST Framework. This API allows users to interact with blog posts and comments through a comprehensive set of endpoints.

## Features

- **Blog Posts Management**: Full CRUD operations for blog posts (Create, Read, Update, Delete)
- **Comments System**: Create, read, and delete comments on posts
- **RESTful Design**: Well-structured API following REST principles using Django REST Framework ViewSets
- **No Authentication Required**: Open API for easy interaction (AllowAny permissions)
- **Pagination**: Built-in pagination support (10 items per page)
- **Different Serializers**: Optimized serializers for list vs detail views (list excludes timestamps)
- **Comprehensive Testing**: Extensive unit tests covering all endpoints and edge cases
- **Admin Interface**: Django admin integration for managing posts and comments
- **Code Quality Tools**: Pre-configured with ruff and pre-commit hooks
- **Development Scripts**: Utility script for initializing development data with sample posts and comments

## Technologies Used

- Python 3.13+
- Django 6.0+
- Django REST Framework 3.16.1+
- SQLite3 (default database)
- uv (for dependency management)
- ruff (code linting and formatting)
- pre-commit (git hooks for code quality)

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

   Alternatively, you can use the initialization script which creates a superuser and sample data:

   ```bash
   python -m scripts.init_dev_data
   ```

   This script creates:
   - A superuser (default: username `admin`, password `admin`, email `admin@example.com`)
   - 5 sample blog posts with content
   - Multiple comments on the posts

   You can customize the superuser credentials using environment variables:
   - `DJANGO_SUPERUSER_USERNAME` (default: `admin`)
   - `DJANGO_SUPERUSER_EMAIL` (default: `admin@example.com`)
   - `DJANGO_SUPERUSER_PASSWORD` (default: `admin`)

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
- **Response:** Paginated list of all posts with fields: `id`, `title`, `content`, `author`
- **Note:**
  - Supports pagination (10 posts per page by default)
  - List view uses a simplified serializer (does not include `created_at` or `updated_at`)
  - Posts are ordered by creation date (newest first)

#### Get Post Details

- **GET** `/api/posts/{id}/`
- **Response:** Post details including `title`, `content`, `created_at`, `updated_at`, `author`

#### Update a Post

- **PUT** `/api/posts/{id}/` - Full update (requires all fields)
- **PATCH** `/api/posts/{id}/` - Partial update (only send fields to update)
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

- `id` (AutoField, primary key)
- `title` (CharField, max_length=200)
- `content` (TextField)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)
- `author` (CharField, max_length=100)
- **Ordering:** Posts are ordered by `-created_at` (newest first)

### Comment Model

- `id` (AutoField, primary key)
- `post` (ForeignKey to Post, CASCADE delete, related_name="comments")
- `content` (TextField)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)
- `author` (CharField, max_length=100)
- **Ordering:** Comments are ordered by `created_at` (oldest first)

## Testing

Run the test suite using:

```bash
python manage.py test
```

The test suite covers:

- Creating posts via API (including validation)
- Creating posts with missing required fields (validation errors)
- Listing posts (with pagination)
- Retrieving post details
- Updating posts (full PUT and partial PATCH)
- Deleting posts
- Error handling (404 for non-existent posts)
- Creating comments (including validation)
- Creating comments with missing required fields
- Creating comments for non-existent posts (404 error)
- Listing comments for a post (only comments for that post)
- Listing comments for posts with no comments (empty list)
- Retrieving comment details
- Deleting comments
- Error handling (404 for non-existent comments)
- Comment validation (ensuring comments belong to correct post)
- Pagination functionality (10 items per page)
- Different serializers for list vs detail views (list excludes timestamps)

## Project Structure

```bash
django-blog/
├── manage.py
├── pyproject.toml
├── Makefile
├── README.md
├── .pre-commit-config.yaml
├── db.sqlite3
├── uv.lock
├── config/              # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── blog/                # Blog app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
└── scripts/              # Utility scripts
    ├── __init__.py
    └── init_dev_data.py  # Script to initialize development data
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

**Update a post (full update):**

```bash
curl -X PUT http://127.0.0.1:8000/api/posts/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Post", "content": "Updated content", "author": "John Doe"}'
```

**Partially update a post:**

```bash
curl -X PATCH http://127.0.0.1:8000/api/posts/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title Only"}'
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

BASE_URL = 'http://127.0.0.1:8000/api'

# Create a post
response = requests.post(f'{BASE_URL}/posts/', json={
    'title': 'My Post',
    'content': 'Post content',
    'author': 'John Doe'
})
print(response.json())

# Get all posts (paginated)
response = requests.get(f'{BASE_URL}/posts/')
print(response.json())  # Returns {'count': ..., 'next': ..., 'previous': ..., 'results': [...]}

# Get post details
response = requests.get(f'{BASE_URL}/posts/1/')
print(response.json())

# Update a post (partial)
response = requests.patch(f'{BASE_URL}/posts/1/', json={
    'title': 'Updated Title'
})
print(response.json())

# Create a comment
response = requests.post(f'{BASE_URL}/posts/1/comments/', json={
    'content': 'Great post!',
    'author': 'Jane Doe'
})
print(response.json())

# List comments for a post
response = requests.get(f'{BASE_URL}/posts/1/comments/')
print(response.json())
```

## Development

### Database

The project uses SQLite3 as the default database (`db.sqlite3`). The database file is created automatically when you run migrations.

### Running Migrations

After making model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

Or use the Makefile shortcut:

```bash
make setup-db
```

### Initializing Development Data

To populate the database with sample data (superuser, posts, and comments):

```bash
python -m scripts.init_dev_data
```

This script:

- Creates a superuser (customizable via environment variables)
- Creates 5 sample blog posts with detailed content
- Creates multiple comments on the posts
- Prints a summary of created data

The script is idempotent - running it multiple times won't create duplicate data.

### Running the Server

Start the development server:

```bash
python manage.py runserver
```

Or use the Makefile shortcut:

```bash
make run
```

This will start the server on `0.0.0.0:8000` (accessible from all network interfaces).

### Code Quality

The project uses `ruff` for linting and formatting, and `pre-commit` for git hooks.

**Run linting and formatting:**

```bash
make run-ruff
```

This runs `ruff check` and `ruff format` on the codebase.

**Run pre-commit checks:**

```bash
make run-pre-commit
```

Or manually:

```bash
uv run pre-commit run --all-files
```

**Pre-commit hooks configured:**

- `check-added-large-files` - Prevents committing large files
- `check-case-conflict` - Detects case conflicts in filenames
- `check-toml` - Validates TOML files
- `debug-statements` - Checks for debugger statements
- `end-of-file-fixer` - Ensures files end with a newline
- `mixed-line-ending` - Fixes line endings (LF)
- `trailing-whitespace` - Removes trailing whitespace
- `ruff` - Runs ruff linter with auto-fix
- `ruff-format` - Formats code with ruff

**Note:** Pre-commit hooks automatically exclude `scripts/`, `migrations/`, `__init__.py`, and `.venv/` directories from ruff checks.

### Accessing Django Admin

If you created a superuser, access the admin panel at:
`http://127.0.0.1:8000/admin/`

The admin interface includes:

- Post management with filtering by date and search functionality
- Comment management with filtering and search

## Evaluation Criteria

This project demonstrates:

- ✅ **API Design**: RESTful principles and well-structured endpoints
- ✅ **Django REST Framework**: Effective use of serializers and views
- ✅ **Testing**: Comprehensive unit tests covering critical functionality
- ✅ **Clean Code**: Well-organized, readable, and maintainable codebase
