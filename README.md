# Library System API

A RESTful API for managing a library system built with Django and Django REST Framework.

## Features

- 📚 Manage Authors
- 📖 Manage Books  
- 👥 Manage Members
- 📋 Track Book Loans
- 🔐 Django Admin Panel

## Installation

1. Clone the repository
```bash
git clone https://github.com/Sir-Nightfallx9/library-system-api.git
cd library-system-api
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies
```bash
pip install django djangorestframework
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run the server
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/

## API Endpoints

- `/api/authors/` - Author management
- `/api/books/` - Book management
- `/api/members/` - Member management
- `/api/loans/` - Loan tracking
- `/admin/` - Django admin panel

## Tech Stack

- Django 6.0
- Django REST Framework
- SQLite

## Author

Sir-Nightfallx9