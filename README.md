# ALX Project Nexus API

## Introduction

ALX Project Nexus is a robust backend API for a job board platform. It connects employers with job seekers, allowing employers to post job adverts and manage applications, and job seekers to browse and apply for jobs. The API is built with Django and Django REST Framework, and it leverages Celery for asynchronous tasks and Docker for containerization.

This README provides a comprehensive guide for frontend developers and code reviewers to understand, set up, and use the API.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Cloning the Repository](#cloning-the-repository)
  - [Environment Configuration](#environment-configuration)
  - [Running with Docker (Recommended)](#running-with-docker-recommended)
  - [Local Development Setup (Without Docker)](#local-development-setup-without-docker)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Job Adverts](#job-adverts)
  - [Job Applications](#job-applications)
  - [Skills](#skills)
  - [Categories](#categories)
- [Data Models](#data-models)
- [Code Style and Conventions](#code-style-and-conventions)
- [Testing](#testing)
- [Contributing](#contributing)

## Features

- **User Authentication:** Secure user registration and login with JWT (JSON Web Tokens).
- **User Profiles:** Users can have profiles with different roles (Employer, Job Seeker, Admin).
- **Job Advert Management:** Employers can create, update, delete, and view job adverts.
- **Job Application System:** Job seekers can apply for jobs with a cover letter and resume.
- **Advanced Filtering and Searching:** Filter and search for jobs based on various criteria like job type, experience level, location, skills, and salary.
- **Asynchronous Tasks:** Celery is used for sending emails (welcome emails, application notifications) asynchronously to avoid blocking API requests.
- **Containerized Environment:** The entire application is containerized with Docker for easy setup and deployment.

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Asynchronous Tasks:** Celery, RabbitMQ
- **Caching:** Redis
- **Containerization:** Docker, Docker Compose
- **API Documentation:** drf-spectacular (for generating OpenAPI schema)

## Project Structure

```
/
├── app/                # Django project configuration
├── core/               # Main Django app for the project
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── logs/               # Log files
├── media/              # User-uploaded files (e.g., resumes)
├── static/             # Static files (CSS, JS, images)
├── .env.example        # Example environment variables
├── docker-compose.yml  # Docker Compose configuration for development
├── Dockerfile          # Dockerfile for the Django application
└── manage.py           # Django's command-line utility
```

## Prerequisites

- [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/install/) (for containerized setup)
- [Python 3.10+](https://www.python.org/downloads/) & [pip](https://pip.pypa.io/en/stable/installation/) (for local setup)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Getting Started

### Cloning the Repository

```bash
git clone https://github.com/codingaday/alx-project-nexus.git
cd alx-project-nexus
```

### Environment Configuration

1.  Create a `.env` file by copying the example file: `cp .env.example .env`
2.  Update the `.env` file with your settings.

| Variable                | Description                                            | Example                                       |
| ----------------------- | ------------------------------------------------------ | --------------------------------------------- |
| `SECRET_KEY`            | A long, random string for Django's secret key.         | `your-super-secret-and-long-random-string`    |
| `DEBUG`                 | Set to `True` for development, `False` for production. | `True`                                        |
| `ALLOWED_HOSTS`         | Comma-separated list of allowed hostnames.             | `localhost,127.0.0.1`                         |
| `DATABASE_URL`          | Connection URL for your PostgreSQL database.           | `postgres://user:password@db:5432/dbname`     |
| `CELERY_BROKER_URL`     | URL for the Celery message broker (RabbitMQ).          | `amqp://guest:guest@rabbitmq:5672//`          |
| `CELERY_RESULT_BACKEND` | URL for the Celery result backend (Redis).             | `redis://redis:6379/0`                        |
| `REDIS_URL`             | URL for the Redis cache.                               | `redis://redis:6379/1`                        |
| `EMAIL_BACKEND`         | Django's email backend.                                | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST`            | SMTP server for sending emails.                        | `smtp.gmail.com`                              |
| `EMAIL_PORT`            | SMTP server port.                                      | `587`                                         |
| `EMAIL_USE_TLS`         | Whether to use TLS for the SMTP connection.            | `True`                                        |
| `EMAIL_HOST_USER`       | Your email address.                                    | `your-email@example.com`                      |
| `EMAIL_HOST_PASSWORD`   | Your email password or app-specific password.          | `your-email-password`                         |
| `DEFAULT_FROM_EMAIL`    | Default "from" address for emails.                     | `noreply@alxprojectnexus.com`                 |
| `CORS_ALLOWED_ORIGINS`  | Comma-separated list of allowed origins for CORS.      | `http://localhost:3000,http://127.0.0.1:3000` |

### Running with Docker (Recommended)

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### Local Development Setup (Without Docker)

1.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run database migrations:**
    ```bash
    python3 manage.py migrate
    ```
4.  **Start the development server:**
    ```bash
    python3 manage.py runserver
    ```

## API Endpoints

The base URL for the API is `/api/`.

### Authentication

#### `POST /auth/register/`

- **Description:** Register a new user.
- **Permissions:** AllowAny
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "user_type": "job_seeker",
    "company_name": "",
    "phone_number": "1234567890",
    "bio": "A short bio.",
    "website": "https://example.com",
    "location": "City, Country"
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "username": "newuser",
    "email": "user@example.com",
    ...
  }
  ```

#### `POST /auth/login/`

- **Description:** Log in a user and receive JWT tokens.
- **Permissions:** AllowAny
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "password": "password123"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "user": { ... },
    "refresh": "...",
    "access": "..."
  }
  ```

### Job Adverts

#### `GET /api/adverts/`

- **Description:** Get a list of all active job adverts.
- **Permissions:** AllowAny
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "title": "Software Engineer",
      ...
    }
  ]
  ```

#### `POST /api/adverts/create/`

- **Description:** Create a new job advert.
- **Permissions:** IsAuthenticated (Employer)
- **Request Body:**
  ```json
  {
    "title": "Senior Backend Developer",
    "description": "...",
    "requirements": "...",
    "location": "Remote",
    "job_type": "full_time",
    "experience_level": "senior",
    "salary_min": 80000,
    "salary_max": 120000,
    "skill_ids": [1, 2],
    "category_ids": [1]
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "id": 2,
    "title": "Senior Backend Developer",
    ...
  }
  ```

### Job Applications

#### `POST /api/adverts/<job_advert_id>/apply/`

- **Description:** Apply for a job.
- **Permissions:** IsAuthenticated (Job Seeker)
- **Request Body:** `multipart/form-data` with `cover_letter` (text) and `resume` (file).
- **Success Response (201 Created):**
  ```json
  {
    "id": 1,
    "job_seeker": { ... },
    "job_advert": { ... },
    "status": "pending",
    ...
  }
  ```

## Data Models

- **User:** Represents a user (employer, job seeker, or admin).
- **JobAdvert:** A job advert posted by an employer.
- **JobApplication:** A job application from a job seeker.
- **Skill:** A skill associated with a job advert.
- **Category:** A category for a job advert.

See `core/models.py` for details.

## Code Style and Conventions

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/). We use `flake8` for linting.

## Testing

Run tests with:

```bash
docker-compose exec app pytest
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue.
