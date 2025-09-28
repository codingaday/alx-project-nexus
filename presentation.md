---
marp: true
theme: default
---

# ALX Project Nexus API

**A Robust Backend for a Modern Job Board**

---

## Introduction

**What is ALX Project Nexus?**

ALX Project Nexus is a powerful and scalable backend API designed to power a modern job board platform. It provides a comprehensive set of features for both employers and job seekers, making it easy to connect talent with opportunities.

**Project Goals:**

- To create a secure and reliable API for a job board.
- To provide a seamless experience for both employers and job seekers.
- To build a scalable and maintainable codebase.

---

## Key Features

- **User Authentication:** Secure JWT-based authentication.
- **Role-Based Access Control:** Different permissions for employers, job seekers, and admins.
- **Job Management:** Full CRUD functionality for job adverts.
- **Application System:** Easy application process for job seekers.
- **Advanced Search & Filtering:** Powerful search and filtering capabilities.
- **Asynchronous Tasks:** Celery for handling background tasks like sending emails.
- **Containerized:** Dockerized for easy setup and deployment.

---

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Asynchronous Tasks:** Celery with RabbitMQ
- **Caching:** Redis
- **Containerization:** Docker, Docker Compose
- **API Documentation:** drf-spectacular

---

## System Architecture

---

## API Endpoints

### Authentication

- `POST /auth/register/`
- `POST /auth/login/`
- `GET /auth/profile/`
- `PUT /auth/profile/`

### Job Adverts

- `GET /api/adverts/`
- `POST /api/adverts/create/`
- `GET /api/adverts/{id}/`
- `PUT /api/adverts/{id}/update/`
- `DELETE /api/adverts/{id}/delete/`

### Job Applications

- `POST /api/adverts/{id}/apply/`
- `GET /api/applications/`
- `GET /api/applications/{id}/`
- `PUT /api/applications/{id}/update/`

### Skills & Categories

- `GET /api/skills/`
- `GET /api/categories/`

---

## Setup and Demo

**1. Clone the Repository:**

```bash
git clone https://github.com/codingaday/alx-project-nexus.git
cd alx-project-nexus
```

**2. Configure Environment:**

```bash
cp .env.example .env
# Edit .env with your settings
```

**3. Run with Docker:**

```bash
docker-compose up --build
```

**Live Demo:** (Showcase API endpoints using a tool like Postman or Insomnia)

---

## Conclusion

ALX Project Nexus provides a solid foundation for building a full-featured job board application.

**Future Work:**

- Real-time notifications with WebSockets.
- Integration with third-party services (e.g., LinkedIn for authentication).
- Advanced analytics for employers.

**Thank you!**
