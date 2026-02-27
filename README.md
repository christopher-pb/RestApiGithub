# 🎓 Student REST API

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JWT](https://img.shields.io/badge/JWT-Auth-orange?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A   **production-ready** Flask REST API featuring **JWT authentication**, comprehensive **Student CRUD operations**, and a clean **Repository Pattern** architecture designed for seamless extensibility from JSON file storage to any database backend.

Built with industry-standard patterns: **Application Factory**, **Blueprints**, **Service Layer**, **Repository Abstraction**, **Docker**, and **GitHub Actions CI/CD**.

---

## 📑 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#1-local-development)
  - [Docker Deployment](#2-docker-deployment)
  - [Environment Variables](#3-environment-variables)
- [API Reference](#-api-reference)
  - [Health Check](#health-check)
  - [Authentication](#authentication)
  - [Students (CRUD)](#students-requires-jwt)
  - [Error Responses](#error-responses)
- [Data Models](#-data-models)
- [Testing](#-testing)
  - [Automated Tests](#automated-tests)
  - [Manual Testing with Postman](#testing-with-postman)
  - [cURL Examples](#quick-test-with-curl)
- [Docker Details](#-docker-details)
- [CI/CD Pipeline](#-cicd-pipeline-github-actions)
- [Security Features](#-security-features)
- [Extending to a Database](#-extending-to-a-database)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Category | Features |
|----------|----------|
| **Authentication** | JWT-based auth with access & refresh tokens, secure password hashing (PBKDF2-SHA256), role-based user management |
| **Student Management** | Full CRUD operations, email uniqueness validation, enrollment tracking, active/inactive status |
| **Architecture** | Repository Pattern, Service Layer, Application Factory, Blueprint-based routing |
| **API Design** | RESTful endpoints, versioned API (`/api/v1`), consistent JSON responses, comprehensive error handling |
| **DevOps** | Docker multi-stage builds, Docker Compose support, GitHub Actions CI/CD, health checks |
| **Testing** | 12+ automated tests, pytest with coverage reports, isolated test fixtures |
| **Security** | Non-root Docker user, token expiration, input validation, error sanitization |

---

## 📁 Project Structure

```
RestApiGithub/
│
├── app/                              # ── Application Package ──
│   ├── __init__.py                   # Application factory (create_app)
│   ├── config.py                     # Environment-based config (dev/test/prod)
│   ├── extensions.py                 # Flask extension instances (JWT)
│   ├── errors.py                     # Global error handlers (400, 401, 404, 500)
│   │
│   ├── api/                          # ── API Layer (Blueprints) ──
│   │   ├── __init__.py
│   │   ├── health.py                 # GET  /api/v1/health
│   │   ├── auth.py                   # POST /api/v1/auth/register & login
│   │   └── students.py               # CRUD /api/v1/students
│   │
│   ├── models/                       # ── Data Models ──
│   │   ├── __init__.py
│   │   ├── user.py                   # User dataclass (id, username, password_hash, role)
│   │   └── student.py                # Student dataclass (id, name, email, course, etc.)
│   │
│   ├── repositories/                 # ── Data Access Layer ──
│   │   ├── __init__.py
│   │   ├── base_repository.py        # Abstract interface (swap JSON → DB here)
│   │   └── json_repository.py        # JSON file-backed implementation
│   │
│   └── services/                     # ── Business Logic Layer ──
│       ├── __init__.py
│       ├── auth_service.py           # Register, login, JWT token generation
│       └── student_service.py        # Student CRUD operations
│
├── tests/                            # ── Test Suite (12 tests) ──
│   ├── conftest.py                   # Shared fixtures (app, client, auth_headers)
│   ├── test_health.py                # Health endpoint test
│   ├── test_auth.py                  # Auth endpoint tests (5 tests)
│   └── test_students.py              # Student endpoint tests (6 tests)
│
├── data/                             # ── Runtime JSON Data Store (git-ignored) ──
│   ├── users.json                    # Created on first user registration
│   └── students.json                 # Created on first student creation
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions: Lint → Test → Zip → Docker
│
├── Dockerfile                        # Multi-stage production build (gunicorn)
├── .dockerignore                     # Files excluded from Docker build
├── docker-compose.yml                # One-command Docker deployment
├── requirements.txt                  # Python dependencies
├── pytest.ini                        # Pytest configuration
├── run.py                            # Development entry point
├── wsgi.py                           # Production WSGI entry (gunicorn)
├── test_api_manual.py                # Manual API test script
├── .env.example                      # Environment variable template
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

---

## 🏗️ Architecture

The project follows the **Repository Pattern** with clear separation of concerns:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   API Layer      │     │  Service Layer   │     │ Repository Layer │     │   Data Store     │
│  (Blueprints)    │ ──▶ │ (Business Logic) │ ──▶ │   (Interface)    │ ──▶ │  (JSON / DB)     │
│                  │     │                  │     │                  │     │                  │
│ health.py        │     │ auth_service.py  │     │ base_repository  │     │ users.json       │
│ auth.py          │     │ student_service  │     │ json_repository  │     │ students.json    │
│ students.py      │     │                  │     │                  │     │                  │
└──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Why this pattern?

| Layer | Responsibility | Benefit |
|-------|----------------|---------|
| **API Layer** | HTTP request/response handling, input validation | Thin controllers, easy to test |
| **Service Layer** | Business logic, data transformation | Reusable across different interfaces |
| **Repository Layer** | Data access abstraction | Swap data stores without code changes |
| **Data Store** | Persistence (JSON/DB) | Flexible storage options |

### Request Flow

```
Client Request
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                     Flask Application                        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   JWT       │    │   Error     │    │   Config    │      │
│  │   Auth      │    │   Handlers  │    │   Manager   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Blueprint (API Layer)                     │
│  • Route definitions                                         │
│  • Request parsing                                           │
│  • Response formatting                                       │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Service Layer                              │
│  • Business logic                                            │
│  • Validation rules                                          │
│  • Token generation                                          │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Repository Layer                            │
│  • CRUD operations                                           │
│  • Data serialization                                        │
│  • Thread-safe operations                                    │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
   Data Store
   (JSON/Database)
```

---

## 🛠️ Tech Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Runtime** | Python | 3.10+ | Programming language |
| **Framework** | Flask | 3.1.x | Web framework |
| **Authentication** | Flask-JWT-Extended | 4.7.x | JWT token handling |
| **Security** | Werkzeug | 3.1.x | Password hashing |
| **Production Server** | Gunicorn | 23.0.x | WSGI HTTP server |
| **Testing** | pytest | 8.3.x | Test framework |
| **Coverage** | pytest-cov | 6.0.x | Code coverage |
| **Linting** | flake8 | 7.1.x | Code quality |
| **Containerization** | Docker | Latest | Container runtime |
| **Orchestration** | Docker Compose | 3.9 | Multi-container apps |

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Required |
|-------------|---------|----------|
| Python | 3.10 or higher | ✅ Yes |
| pip | Latest | ✅ Yes |
| Docker | Latest | ⚡ Optional |
| Docker Compose | v2+ | ⚡ Optional |
| Git | Latest | ⚡ Optional |

### 1. Local Development

```bash
# Clone the repository
git clone https://github.com/<your-username>/RestApiGithub.git
cd RestApiGithub

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Windows (CMD)
venv\Scripts\activate.bat
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
python run.py
```

The API is now running at **http://localhost:5000**

#### Verify Installation

```bash
# Check health endpoint
curl http://localhost:5000/api/v1/health

# Expected response:
# {"status":"healthy","timestamp":"2026-02-20T..."}
```

### 2. Docker Deployment

#### Using Docker Compose (Recommended)

```bash
# Build and start in foreground
docker-compose up --build

# Build and start in background
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

#### Standalone Docker

```bash
# Build the image
docker build -t student-api .

# Run the container
docker run -p 5000:5000 \
  -e SECRET_KEY=my-secret-key \
  -e JWT_SECRET_KEY=jwt-secret-key \
  -v student-data:/app/data \
  --name student-api \
  student-api

# Check logs
docker logs -f student-api

# Stop the container
docker stop student-api

# Remove the container
docker rm student-api
```

### 3. Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `FLASK_ENV` | `development` | Environment mode: `development`, `testing`, `production` | No |
| `SECRET_KEY` | `change-me-in-production` | Flask secret key for session signing | **Yes (prod)** |
| `JWT_SECRET_KEY` | `jwt-change-me-in-production` | Secret key for JWT token signing | **Yes (prod)** |
| `JWT_ACCESS_TOKEN_HOURS` | `1` | Access token validity period in hours | No |
| `JWT_REFRESH_TOKEN_DAYS` | `30` | Refresh token validity period in days | No |
| `PORT` | `5000` | Server listening port | No |
| `DATA_DIR` | `./data` | Directory for JSON data storage | No |

> ⚠️ **Security Warning**: Always use strong, unique values for `SECRET_KEY` and `JWT_SECRET_KEY` in production!

---

## 🔐 API Reference

**Base URL:** `http://localhost:5000/api/v1`

**Content-Type:** `application/json`

### Health Check

Check if the API is running and healthy.

| Method | Endpoint | Auth Required | Rate Limited |
|--------|----------|---------------|--------------|
| GET | `/health` | ❌ No | ❌ No |

#### Response

```http
GET /api/v1/health
```

```json
{
  "status": "healthy",
  "timestamp": "2026-02-20T10:30:00+00:00"
}
```

---

### Authentication

#### Register User

Create a new user account.

| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| POST | `/auth/register` | ❌ No |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ Yes | Unique username (min 1 char) |
| `password` | string | ✅ Yes | User password (min 1 char) |
| `role` | string | ❌ No | User role (default: `"user"`) |

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "admin",
  "password": "Admin123!",
  "role": "admin"
}
```

**Success Response (201 Created):**

```json
{
  "message": "User registered successfully",
  "user": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "username": "admin",
    "role": "admin"
  }
}
```

**Error Responses:**

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Missing username or password | `{"error": "username and password are required"}` |
| 409 | Username already exists | `{"error": "Username already exists"}` |

---

#### Login

Authenticate and receive JWT tokens.

| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| POST | `/auth/login` | ❌ No |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ Yes | Registered username |
| `password` | string | ✅ Yes | User password |

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "Admin123!"
}
```

**Success Response (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "username": "admin",
    "role": "admin"
  }
}
```

**Error Responses:**

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Missing credentials | `{"error": "username and password are required"}` |
| 401 | Invalid credentials | `{"error": "Invalid username or password"}` |

> 📌 **Important:** Copy the `access_token` from the login response. Use it in the `Authorization` header for all protected endpoints.

---

### Students (Requires JWT)

All student endpoints require authentication via Bearer token:

```http
Authorization: Bearer <access_token>
```

#### List All Students

| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| GET | `/students` | ✅ Yes |

```http
GET /api/v1/students
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response (200 OK):**

```json
{
  "count": 2,
  "students": [
    {
      "id": "f5e6d7c8-...",
      "first_name": "Alice",
      "last_name": "Smith",
      "email": "alice@university.com",
      "course": "Computer Science",
      "enrollment_date": "2026-02-13T10:30:00+00:00",
      "is_active": true
    },
    {
      "id": "a1b2c3d4-...",
      "first_name": "Bob",
      "last_name": "Johnson",
      "email": "bob@university.com",
      "course": "Mathematics",
      "enrollment_date": "2026-02-14T09:15:00+00:00",
      "is_active": true
    }
  ]
}
```

---

#### Get Student by ID

| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| GET | `/students/<id>` | ✅ Yes |

```http
GET /api/v1/students/f5e6d7c8-1234-5678-abcd-ef1234567890
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response (200 OK):**

```json
{
  "id": "f5e6d7c8-1234-5678-abcd-ef1234567890",
  "first_name": "Alice",
  "last_name": "Smith",
  "email": "alice@university.com",
  "course": "Computer Science",
  "enrollment_date": "2026-02-13T10:30:00+00:00",
  "is_active": true
}
```

**Error Response (404 Not Found):**

```json
{
  "error": "Student not found"
}
```

---

#### Create Student

| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| POST | `/students` | ✅ Yes |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `first_name` | string | ✅ Yes | Student's first name |
| `last_name` | string | ✅ Yes | Student's last name |
| `email` | string | ✅ Yes | Unique email address |
| `course` | string | ✅ Yes | Enrolled course name |

```http
POST /api/v1/students
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "first_name": "Alice",
  "last_name": "Smith",
  "email": "alice@university.com",
  "course": "Computer Science"
}
```

**Response (201 Created):**

```json
{
  "message": "Student created",
  "student": {
    "id": "f5e6d7c8-1234-5678-abcd-ef1234567890",
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice@university.com",
    "course": "Computer Science",
    "enrollment_date": "2026-02-20T10:30:00+00:00",
    "is_active": true
  }
}
```

**Error Responses:**

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Missing required fields | `{"error": "Missing fields: first_name, email"}` |
| 409 | Email already exists | `{"error": "A student with this email already exists"}` |

---

#### Update Student

| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| PUT | `/students/<id>` | ✅ Yes |

**Request Body (all fields optional):**

| Field | Type | Description |
|-------|------|-------------|
| `first_name` | string | Updated first name |
| `last_name` | string | Updated last name |
| `email` | string | Updated email |
| `course` | string | Updated course |
| `is_active` | boolean | Active status |

```http
PUT /api/v1/students/f5e6d7c8-1234-5678-abcd-ef1234567890
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "course": "Data Science",
  "is_active": false
}
```

**Response (200 OK):**

```json
{
  "message": "Student updated",
  "student": {
    "id": "f5e6d7c8-1234-5678-abcd-ef1234567890",
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice@university.com",
    "course": "Data Science",
    "enrollment_date": "2026-02-13T10:30:00+00:00",
    "is_active": false
  }
}
```

---

#### Delete Student

| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| DELETE | `/students/<id>` | ✅ Yes |

```http
DELETE /api/v1/students/f5e6d7c8-1234-5678-abcd-ef1234567890
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response (200 OK):**

```json
{
  "message": "Student deleted"
}
```

---

### Error Responses

All API errors follow a consistent format:

```json
{
  "error": "Error type",
  "message": "Detailed error description"
}
```

| Status Code | Error Type | Common Causes |
|-------------|------------|---------------|
| 400 | Bad Request | Missing required fields, invalid JSON |
| 401 | Unauthorized | Missing/invalid/expired JWT token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate username or email |
| 422 | Unprocessable Entity | Validation failed |
| 500 | Internal Server Error | Server-side error (details logged) |

---

## 📊 Data Models

### User Model

```python
@dataclass
class User:
    id: str              # UUID v4 (auto-generated)
    username: str        # Unique username
    password_hash: str   # PBKDF2-SHA256 hashed password
    role: str = "user"   # User role (default: "user")
```

**JSON Storage Format:**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "username": "admin",
  "password_hash": "pbkdf2:sha256:600000$...",
  "role": "admin"
}
```

### Student Model

```python
@dataclass
class Student:
    id: str                    # UUID v4 (auto-generated)
    first_name: str            # Student's first name
    last_name: str             # Student's last name
    email: str                 # Unique email address
    course: str                # Enrolled course
    enrollment_date: str       # ISO 8601 timestamp (auto-generated)
    is_active: bool = True     # Active status (default: True)
```

**JSON Storage Format:**

```json
{
  "id": "f5e6d7c8-1234-5678-abcd-ef1234567890",
  "first_name": "Alice",
  "last_name": "Smith",
  "email": "alice@university.com",
  "course": "Computer Science",
  "enrollment_date": "2026-02-20T10:30:00+00:00",
  "is_active": true
}
```

---

## 🧪 Testing

### Automated Tests

The project includes **12+ automated tests** covering all endpoints:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_students.py -v

# Run with coverage report
pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

**Test Coverage Breakdown:**

| Test File | Tests | Description |
|-----------|-------|-------------|
| `test_health.py` | 1 | Health endpoint verification |
| `test_auth.py` | 5 | Registration, duplicate handling, login, authentication |
| `test_students.py` | 6 | CRUD operations, authorization checks |

**Test Fixtures:**

```python
# tests/conftest.py
@pytest.fixture
def app():
    """Create test application instance."""
    
@pytest.fixture
def client(app):
    """Create test client."""
    
@pytest.fixture
def auth_headers(client):
    """Get authentication headers for protected endpoints."""
```

### Testing with Postman

#### Step-by-step Workflow:

1. **Register a new user**
   - `POST http://localhost:5000/api/v1/auth/register`
   - Body: `{"username": "testuser", "password": "Test123!"}`

2. **Login to get tokens**
   - `POST http://localhost:5000/api/v1/auth/login`
   - Body: `{"username": "testuser", "password": "Test123!"}`
   - Copy the `access_token` from response

3. **Configure Authorization**
   - Go to **Authorization** tab
   - Select **Bearer Token**
   - Paste the access token

4. **Test Student Endpoints**
   - Now you can access all `/students` endpoints

#### Import Postman Collection

Create a Postman collection with these requests:

```
📁 Student API
├── 🟢 Health Check
│   └── GET {{base_url}}/health
├── 📁 Auth
│   ├── POST {{base_url}}/auth/register
│   └── POST {{base_url}}/auth/login
└── 📁 Students
    ├── GET {{base_url}}/students
    ├── GET {{base_url}}/students/:id
    ├── POST {{base_url}}/students
    ├── PUT {{base_url}}/students/:id
    └── DELETE {{base_url}}/students/:id
```

### Quick Test with cURL

```bash
# 1. Register a new user
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}'

# 2. Login and save token
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}' | jq -r '.access_token')

# 3. Create a student
curl -X POST http://localhost:5000/api/v1/students \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "course": "CS"}'

# 4. List all students
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/students

# 5. Get a specific student (replace STUDENT_ID)
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/students/<STUDENT_ID>

# 6. Update a student
curl -X PUT http://localhost:5000/api/v1/students/<STUDENT_ID> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"course": "Data Science"}'

# 7. Delete a student
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/students/<STUDENT_ID>
```

#### PowerShell Alternative

```powershell
# Register
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/register" `
  -Method POST -ContentType "application/json" `
  -Body '{"username": "admin", "password": "Admin123!"}'

# Login
$login = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/login" `
  -Method POST -ContentType "application/json" `
  -Body '{"username": "admin", "password": "Admin123!"}'

$token = $login.access_token

# Create Student
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/students" `
  -Method POST -ContentType "application/json" `
  -Headers @{Authorization = "Bearer $token"} `
  -Body '{"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "course": "CS"}'

# List Students
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/students" `
  -Headers @{Authorization = "Bearer $token"}
```

---

## 🐳 Docker Details

### Dockerfile Features

| Feature | Description |
|---------|-------------|
| **Multi-stage build** | Smaller final image (~150MB) |
| **Non-root user** | Runs as `appuser` for security |
| **Gunicorn** | Production WSGI server with 4 workers |
| **Health check** | Built-in `HEALTHCHECK` instruction |
| **Slim base** | `python:3.12-slim` for minimal footprint |

### Dockerfile Breakdown

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
# Install Python packages to /install prefix

# Stage 2: Production image
FROM python:3.12-slim AS production
# Create non-root user
# Copy only necessary files
# Configure health check
# Run with Gunicorn
```

### Docker Commands Reference

```bash
# Build image
docker build -t student-api .

# Build with no cache
docker build --no-cache -t student-api .

# Run container (foreground)
docker run -p 5000:5000 \
  -e SECRET_KEY=my-secret \
  -e JWT_SECRET_KEY=jwt-secret \
  student-api

# Run container (background)
docker run -d -p 5000:5000 \
  -e SECRET_KEY=my-secret \
  -e JWT_SECRET_KEY=jwt-secret \
  --name student-api \
  student-api

# View running containers
docker ps

# View logs
docker logs student-api
docker logs -f student-api  # Follow logs

# Execute command in container
docker exec -it student-api /bin/bash

# Stop container
docker stop student-api

# Remove container
docker rm student-api

# Remove image
docker rmi student-api
```

### Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs
docker-compose logs -f api  # Follow specific service

# Stop services
docker-compose stop

# Stop and remove
docker-compose down

# Stop, remove, and delete volumes
docker-compose down -v

# View running services
docker-compose ps
```

---

## 📦 CI/CD Pipeline (GitHub Actions)

The workflow at `.github/workflows/ci.yml` runs on every push to `main`/`develop` and on pull requests:

```
┌─────────┐     ┌─────────┐     ┌─────────────┐     ┌──────────────┐
│  Lint   │ ──▶ │  Test   │ ──▶ │ Build & Zip │ ──▶ │ Docker Build │
│ (flake8)│     │ (pytest)│     │  (artifact) │     │  (verify)    │
└─────────┘     └─────────┘     └─────────────┘     └──────────────┘
                     │                 │                    │
                     ▼                 ▼                    ▼
              📊 Coverage       📦 student-api.zip    🐳 Docker image
                 Report         (artifact download)     (health check)
```

### Pipeline Stages

| Stage | Tool | Purpose | Failure Action |
|-------|------|---------|----------------|
| **Lint** | flake8 | Static code analysis | ❌ Block merge |
| **Test** | pytest | Run automated tests | ❌ Block merge |
| **Coverage** | pytest-cov | Generate coverage report | 📊 Upload artifact |
| **Build** | zip | Create deployable package | 📦 Upload artifact |
| **Docker** | docker build | Verify container builds | ❌ Block merge |

### Triggering Workflows

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

---

## 🛡️ Security Features

| Feature | Implementation | Details |
|---------|----------------|---------|
| **Password Hashing** | PBKDF2-SHA256 | Werkzeug's `generate_password_hash()` |
| **JWT Tokens** | HS256 signing | Short-lived access (1h), long-lived refresh (30d) |
| **Protected Endpoints** | `@jwt_required()` | All student APIs require valid token |
| **Non-root Docker** | `appuser` | Container runs as unprivileged user |
| **Error Sanitization** | Custom handlers | 500 errors never leak internal details |
| **Input Validation** | Service layer | All inputs validated before processing |
| **Thread Safety** | Locking | JSON repository uses threading locks |

### Security Best Practices

1. **Always change default secrets in production**
   ```bash
   export SECRET_KEY=$(openssl rand -hex 32)
   export JWT_SECRET_KEY=$(openssl rand -hex 32)
   ```

2. **Use HTTPS in production** (configure reverse proxy)

3. **Implement rate limiting** for auth endpoints (future enhancement)

4. **Regular dependency updates**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## 🔌 Extending to a Database

The project is designed to swap from JSON files to any database with **zero changes** to API or service code:

### Step 1: Create New Repository Implementation

```python
# app/repositories/sqlalchemy_repository.py
from typing import Optional, TypeVar, Type
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository

T = TypeVar("T")

class SQLAlchemyRepository(BaseRepository[T]):
    """SQLAlchemy-backed repository implementation."""
    
    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    def get_all(self) -> list[T]:
        return self._session.query(self._model_cls).all()

    def get_by_id(self, entity_id: str) -> Optional[T]:
        return self._session.query(self._model_cls).get(entity_id)

    def create(self, entity: T) -> T:
        self._session.add(entity)
        self._session.commit()
        return entity

    def update(self, entity_id: str, entity: T) -> Optional[T]:
        existing = self.get_by_id(entity_id)
        if existing:
            # Update fields
            self._session.commit()
        return existing

    def delete(self, entity_id: str) -> bool:
        entity = self.get_by_id(entity_id)
        if entity:
            self._session.delete(entity)
            self._session.commit()
            return True
        return False
```

### Step 2: Update Blueprint to Use New Repository

```python
# app/api/students.py
def _get_service() -> StudentService:
    # Option 1: JSON (current)
    # repo = JsonRepository[Student](filepath, Student)
    
    # Option 2: SQLAlchemy
    # repo = SQLAlchemyRepository[Student](db.session, StudentModel)
    
    return StudentService(repo)
```

### Supported Database Options

| Database | Package | Use Case |
|----------|---------|----------|
| PostgreSQL | `psycopg2-binary`, `SQLAlchemy` | Production, relational data |
| MySQL | `pymysql`, `SQLAlchemy` | Production, relational data |
| MongoDB | `pymongo` | Document storage, flexible schema |
| SQLite | Built-in | Development, small deployments |
| Redis | `redis` | Caching, session storage |

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```
Error: Address already in use (port 5000)
```

**Solution:**
```bash
# Find process using port
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux

# Kill process or use different port
python run.py  # Uses PORT env variable
```

#### 2. JWT Token Expired

```json
{"error": "Token has expired"}
```

**Solution:** Login again to get a new access token.

#### 3. Missing Authorization Header

```json
{"error": "Missing Authorization Header"}
```

**Solution:** Include the Bearer token:
```bash
curl -H "Authorization: Bearer <your_token>" ...
```

#### 4. Docker Build Fails

```
Error: pip install failed
```

**Solution:**
```bash
# Clear Docker cache
docker builder prune
docker build --no-cache -t student-api .
```

#### 5. Tests Fail with Import Error

```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
```bash
# Ensure you're in the project root
cd RestApiGithub

# Install in development mode
pip install -e .
# Or run from project root
python -m pytest
```

### Debug Mode

Enable detailed logging:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### 1. Fork and Clone

```bash
git clone https://github.com/<your-username>/RestApiGithub.git
cd RestApiGithub
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Follow existing code style
- Add tests for new features
- Update documentation

### 4. Run Quality Checks

```bash
# Lint
flake8 app tests

# Test
pytest -v

# Coverage
pytest --cov=app --cov-report=term-missing
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

- Open PR against `develop` branch
- Describe your changes
- Wait for CI checks to pass
- Request review

### Commit Message Convention

```
<type>(<scope>): <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance
```

---

## 📝 Data Storage

Data is stored as JSON files in the `data/` directory (auto-created at runtime):

| File | Contents | Notes |
|------|----------|-------|
| `users.json` | Registered user accounts | Passwords are hashed |
| `students.json` | Student records | Auto-generated enrollment date |

The `data/` folder is:
- ✅ Git-ignored (not committed to repository)
- ✅ Persisted via Docker volume in containerized deployments
- ✅ Thread-safe with file locking

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/<your-username>/RestApiGithub/issues)
- **Discussions**: [GitHub Discussions](https://github.com/<your-username>/RestApiGithub/discussions)

---

<p align="center">
  Made with ❤️ using Flask
</p>
