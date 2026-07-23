# Mini Library Management System
Backend assignment for Imagio Creations Pvt. Ltd. — a REST API for managing
library authors, books, members, and borrowing, built with Django REST Framework.

## Features

- JWT Authentication
- Role-based authorization (Librarian & Member)
- Author management
- Book management
- Member management
- Book borrowing and return
- Fine calculation for overdue books
- Member suspension
- Search, ordering, and pagination
- Service-layer architecture for business logic

## Roles

The system supports two roles:

- Librarian
  - Manage authors
  - Manage books
  - Manage members

- Member
  - Browse books
  - Borrow books
  - Return books
  - Pay overdue fines

## Tech Stack
- Python 3.14.2
- Django 5.2.12
- Django Rest Framework
- PostgreSQL
- JWT Authentication (djangorestframework-simplejwt)

## Project Structure
```text
mini-library-management-system
├── apps
│   ├── authors
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── books
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── borrowings
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── common
│   │   ├── pagination.py
│   │   └── permissions.py
│   ├── members
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── users
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── managers.py
│       ├── migrations
│       ├── models.py
│       ├── tests.py
│       └── views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
└── manage.py
```

## Setup
1. **Clone the repository**
```bash
   git clone https://github.com/manoj-pun/mini-library-management-system.git
   cd mini-library-management-system
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv

   # macOS/Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
```

3. **Copy the environment file and fill in your values**
```bash
   cp .env.example .env
```

4. **Create the PostgreSQL database**
```bash
   createdb -U postgres library_db
```

5. **Install dependencies**
```bash
   pip install -r requirements.txt
```

6. **Run migrations**
```bash
   python manage.py migrate
```

7. **Create a librarian account**
```bash
   python manage.py createsuperuser
```

8. **Run the server**
```bash
   python manage.py runserver
```

The API is now available at http://localhost:8000/.

## API Documentation

Interactive Swagger documentation is available after running the project:

http://localhost:8000/api/schema/swagger-ui

