# 🎯 ALX Project Nexus

> **Connecting Talent with Opportunity**

A professional job board platform that bridges the gap between employers and skilled professionals. Built with Django REST Framework for reliable, scalable job matching and application management.

[![CI/CD Pipeline](https://github.com/codingaday/alx-project-nexus/actions/workflows/ci.yml/badge.svg)](https://github.com/codingaday/alx-project-nexus/actions/workflows/ci.yml)
[![Code Coverage](https://codecov.io/gh/codingaday/alx-project-nexus/branch/main/graph/badge.svg)](https://codecov.io/gh/codingaday/alx-project-nexus)
![Django](https://img.shields.io/badge/django-5.2.6-blue)
![License](https://img.shields.io/badge/license-ALX-orange)

---

## 🚀 What is ALX Project Nexus?

**ALX Project Nexus** is a comprehensive job marketplace that empowers:

- **🏢 Employers** to find perfect talent matches and manage job applications
- **👥 Job Seekers** to discover opportunities and apply professionally
- **📊 Teams** to streamline recruitment workflows with automated notifications

### ✨ Key Benefits

- **🚀 Fast Setup**: Pre-configured API with comprehensive documentation
- **🔧 Customizable**: Flexible user roles, skill matching, and workflows
- **📱 API-First**: Easy integration with existing hiring platforms
- **🔒 Secure**: Production-ready authentication and data handling
- **⚡ Automated**: Background email notifications and task processing

---

## 👥 Who Uses ALX Project Nexus?

### 🏢 For Employers

- Post unlimited job opportunities
- Review applications with detailed candidate profiles
- Automate interview scheduling with applicant notifications
- Track application progress and interview outcomes

### 👤 For Job Seekers

- Browse curated job listings by skills and location
- Submit professional applications with cover letters
- Track application status in real-time
- Receive updates on application reviews and interviews

---

## 📚 Getting Started

### 🔗 Base API URL

```
https://alx-project-nexus-5-ivj6.onrender.com/
```

### 🔐 Authentication Required

Most endpoints require JWT authentication. Include the token in headers:

```bash
Authorization: Bearer your-jwt-token-here
```

### 🌐 API Documentation

**Interactive Swagger Docs**: `https://alx-project-nexus-5-ivj6.onrender.com/api/docs/`

- Test endpoints directly from the browser
- Generate API keys and explore specifications
- No coding required to understand functionality

---

## 🗝️ Authentication Flow

### 1. New User Registration

```http
POST /auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john.doe@email.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "user_type": "job_seeker",  // or "employer"
  "company_name": "(optional for employers)",
  "phone_number": "+1234567890"
}
```

**Response:**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john.doe@email.com",
  "user_type": "job_seeker",
  "is_active": true
}
```

### 2. User Login

```http
POST /auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1Q...",
  "refresh": "eyJ0eXAiOiJKV1..."
}
```

### 3. Access Profile Information

```http
GET /auth/profile/
Authorization: Bearer your-access-token
```

---

## 💼 Job Board Features

### 🔍 Browse Job Listings

**Get All Available Jobs**

```http
GET /api/adverts/
Authorization: Bearer your-access-token
```

**Query Parameters:**

- `search=python` - Search by keywords
- `location=new+york` - Filter by location
- `job_type=full_time` - Filter by employment type
- `experience_level=mid` - Junior/Senior/Executive
- `skills=python,django` - Required skills
- `categories=technology,engineering` - Job categories

**Example with Filters:**

```http
GET /api/adverts/?search=django&location=remote&job_type=full_time
```

**Response:**

```json
{
  "results": [
    {
      "id": 1,
      "title": "Senior Django Developer",
      "company_name": "Tech Corp",
      "location": "Remote",
      "salary_range": "$80k - $120k",
      "experience_level": "Senior",
      "is_active": true,
      "created_at": "2025-09-29T10:00:00Z"
    }
  ],
  "count": 1,
  "next": null,
  "previous": null
}
```

---

## 🏢 Employer Dashboard

### 📝 Create Job Posting

```http
POST /api/adverts/create/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "title": "Senior Python Developer",
  "description": "Join our team building cutting-edge applications...",
  "requirements": "5+ years experience, Python expertise...",
  "location": "New York, NY",
  "job_type": "full_time",
  "experience_level": "senior",
  "salary_min": 90000,
  "salary_max": 130000,
  "salary_currency": "USD",
  "is_remote": false,
  "application_deadline": "2025-12-31",
  "skill_ids": [1, 3, 5],     // Python, Django, PostgreSQL
  "category_ids": [1, 2]       // Technology, Backend Development
}
```

### 📋 Manage Posted Jobs

```http
GET /api/adverts/?my_jobs=true
Authorization: Bearer your-access-token
```

**Update Job Posting:**

```http
PUT /api/adverts/{job_id}/update/
Authorization: Bearer your-access-token

{
  "title": "Updated Title",
  "is_active": false  // Close the position
}
```

---

## 👥 Candidate Applications

### 📤 Submit Job Application

```http
POST /api/adverts/{job_id}/apply/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "cover_letter": "Dear Hiring Manager,\n\nI am excited to apply for...",
  "resume": "(File upload - multipart/form-data)"
}
```

**Upload Resume:**

```bash
curl -X POST \
  https://your-domain.com/api/adverts/123/apply/ \
  -H "Authorization: Bearer your-token" \
  -F "cover_letter=Your cover letter text here" \
  -F "resume=@path/to/your/resume.pdf"
```

### 📊 Track Application Status

**View Your Applications:**

```http
GET /api/applications/
Authorization: Bearer your-access-token
```

**Response:**

```json
[
  {
    "id": 456,
    "job_advert": {
      "id": 123,
      "title": "Senior Developer",
      "employer": "Tech Corp"
    },
    "status": "review", // pending, review, interview, accepted, rejected
    "applied_at": "2025-09-29T15:30:00Z",
    "updated_at": "2025-09-30T09:00:00Z"
  }
]
```

---

## 🏢 Managing Applications (Employers)

### 📬 Review Incoming Applications

```http
GET /api/applications/
Authorization: Bearer your-access-token
```

**Filter by Job:**

```http
GET /api/applications/?job_advert_id=123&status=pending
```

### 📞 Update Application Status

```http
PUT /api/applications/{application_id}/update/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "status": "interview",  // Update status
  "notes": "Excellent technical skills, schedule interview"
}
```

---

## 📧 Automated Email System

### 🎯 What Gets Automated?

- **Welcome Emails**: New user registration confirmation
- **Application Notifications**: Employers receive instant alerts for new applications
- **Status Updates**: Candidates notified of application progress
- **Interview Scheduling**: Automated communication for interview processes

### ⏰ Processing Time

Email notifications are sent asynchronously using background workers, ensuring:

- ⚡ Instant API responses
- 🔄 Reliable delivery (retries on failure)
- 📈 Scalable processing (handles multiple applications simultaneously)

---

## 🎨 Advanced Features

### 🔍 Smart Job Matching

**Skill-Based Filtering:**

```http
GET /api/adverts/?skills_required=python&min_skill_importance=4
```

**Location Preferences:**

```http
GET /api/adverts/?is_remote=true&location=willing_to_relocate
```

### 📈 Analytics Ready

Built-in counters track:

- Job view statistics (`views_count`)
- Application volume (`applications_count`)
- Success rates and engagement metrics

---

## 🚨 Error Handling

### Common HTTP Status Codes

- **200**: Success - Request completed
- **201**: Created - Resource successfully created
- **400**: Bad Request - Invalid data provided
- **401**: Unauthorized - Authentication required
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource doesn't exist

### Error Response Format

```json
{
  "detail": "Authentication credentials were not provided.",
  "code": "not_authenticated"
}
```

---

## 🔧 Technical Specifications

- **Framework**: Django 5.2.6 with Django REST Framework 3.16.1
- **Authentication**: JWT (JSON Web Tokens) with refresh tokens
- **Database**: PostgreSQL with optimized relationships
- **Caching**: Redis for session and data caching
- **Background Jobs**: Celery with RabbitMQ message broker
- **File Storage**: Configurable media storage for resumes
- **Email**: SMTP integration with HTML template support

---

## 🏆 Best Practices

### For Job Postings

- **Clear Descriptions**: Use detailed, specific requirements
- **Realistic Expectations**: Set accurate salary ranges and skill requirements
- **Timely Updates**: Keep application deadlines current
- **Professional Information**: Include company culture and growth opportunities

### For Applications

- **Tailored Applications**: Customize cover letters for each position
- **Complete Profiles**: Include contact information and professional details
- **Professional Documents**: Upload recent resumes and portfolio materials

---

## 🆘 Support & Troubleshooting

### Common Issues

**"Authentication Required"**
→ Ensure you're sending the Authorization header
→ Check token expiration (access tokens expire in 30 minutes)

**"Application Deadline Passed"**
→ Job posting deadlines are enforced by the system
→ Contact employer directly if deadline extension is available

**"File Upload Failed"**
→ Supported formats: PDF, DOC, DOCX (max 5MB)
→ Check file size and format requirements

---

## 📞 API Status & Monitoring

- **Health Check**: Standard Django health checks available
- **Performance**: Optimized queries with database indexing
- **Scaling**: Redis caching reduces database load
- **Background Processing**: Celery ensures stable API performance


## 🚀 Getting Started Today

1. **Register** an account at `/auth/register/`
2. **Explore** jobs with `/api/adverts/`
3. **Apply** to positions using `/api/adverts/{id}/apply/`
4. **Track** your progress at `/api/applications/`

**API Documentation:** `https://alx-project-nexus-5-ivj6.onrender.com/api/docs/`

---

_Built with ❤️ for the ALX Software Engineering community. Connect, grow, and succeed together!_ 🌟
