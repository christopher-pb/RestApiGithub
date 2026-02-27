# Complete Lab Guide: PostgreSQL + pgAdmin + Student REST API with Docker

> **Audience:** Students learning DevOps, Docker, and REST API development.
> This guide walks you through **every step** — from installing prerequisites to
> testing your fully deployed containerised application.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Architecture Overview](#2-architecture-overview)
3. [Part A — Run PostgreSQL in Docker](#3-part-a--run-postgresql-in-docker)
4. [Part B — Install & Configure pgAdmin](#4-part-b--install--configure-pgadmin)
5. [Part C — Create the Database Schema Manually](#5-part-c--create-the-database-schema-manually)
6. [Part D — Explore SQL Queries](#6-part-d--explore-sql-queries)
7. [Part E — Deploy the Full Stack with Docker Compose](#7-part-e--deploy-the-full-stack-with-docker-compose)
8. [Part F — Test the API with cURL / Postman](#8-part-f--test-the-api-with-curl--postman)
9. [Part G — Inspect & Debug](#9-part-g--inspect--debug)
10. [Part H — Clean Up](#10-part-h--clean-up)
11. [Quick Reference: All Commands](#11-quick-reference--all-commands)
12. [Troubleshooting](#12-troubleshooting)
13. [Appendix: SQL Queries Cheat-Sheet](#13-appendix--sql-queries-cheat-sheet)

---

## 1. Prerequisites

| Tool | Minimum Version | Download |
|------|----------------|----------|
| **Docker Desktop** | 4.x+ | <https://www.docker.com/products/docker-desktop/> |
| **Git** | 2.x+ | <https://git-scm.com/downloads> |
| **Postman** *(optional)* | Latest | <https://www.postman.com/downloads/> |

After installing Docker Desktop, verify it's running:

```powershell
docker --version
docker compose version
```

> **Windows Users:** Make sure WSL 2 backend is enabled in Docker Desktop settings.

---

## 2. Architecture Overview

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────────┐
│              │       │                  │       │                  │
│   Browser /  │──────►│  Flask REST API   │──────►│   PostgreSQL 16  │
│   Postman    │ :5000 │  (student-api)   │ :5432 │  (student-api-db)│
│              │       │                  │       │                  │
└──────────────┘       └──────────────────┘       └──────────────────┘
                                                          │
                       ┌──────────────────┐               │
                       │    pgAdmin 4     │───────────────┘
                       │   (browser UI)   │ :5050
                       └──────────────────┘
```

| Container | Image | Port | Purpose |
|-----------|-------|------|---------|
| `student-api-db` | `postgres:16-alpine` | `5432` | PostgreSQL database |
| `student-api` | Built from `Dockerfile` | `5000` | Flask REST API |
| `pgadmin` | `dpage/pgadmin4` | `5050` | Database GUI |

---

## 3. Part A — Run PostgreSQL in Docker

In this section you will start **only** the PostgreSQL container, so you can
learn how to work with it before deploying the full application.

### Step 1 — Pull the PostgreSQL Image

```powershell
docker pull postgres:16-alpine
```

### Step 2 — Create a Docker Network

A dedicated network lets containers talk to each other by name.

```powershell
docker network create student-net
```

### Step 3 — Start the PostgreSQL Container

```powershell
docker run -d `
    --name student-api-db `
    --network student-net `
    -e POSTGRES_USER=student_api `
    -e POSTGRES_PASSWORD=student_api `
    -e POSTGRES_DB=student_api_db `
    -p 5432:5432 `
    -v pg-data:/var/lib/postgresql/data `
    postgres:16-alpine
```

> **What each flag means:**
>
> | Flag | Purpose |
> |------|---------|
> | `-d` | Run in the background (detached) |
> | `--name` | Give the container a human-readable name |
> | `--network` | Attach to our custom network |
> | `-e` | Set environment variables (user, password, database) |
> | `-p 5432:5432` | Expose port 5432 on your machine |
> | `-v pg-data:...` | Persist data in a Docker volume |

### Step 4 — Verify the Container is Running

```powershell
docker ps
```

You should see `student-api-db` with status `Up`.

### Step 5 — Test the Connection from Terminal

```powershell
docker exec -it student-api-db psql -U student_api -d student_api_db
```

You are now inside the PostgreSQL interactive shell. Try:

```sql
SELECT version();
\q
```

> `\q` exits the `psql` shell.

---

## 4. Part B — Install & Configure pgAdmin

pgAdmin is a free, web-based GUI for managing PostgreSQL databases.

### Option 1 — Run pgAdmin in Docker (Recommended)

```powershell
docker run -d `
    --name pgadmin `
    --network student-net `
    -e PGADMIN_DEFAULT_EMAIL=admin@example.com `
    -e PGADMIN_DEFAULT_PASSWORD=admin123 `
    -p 5050:80 `
    dpage/pgadmin4
```

Now open your browser and go to: **http://localhost:5050**

### Option 2 — Install pgAdmin Natively

1. Download from <https://www.pgadmin.org/download/>
2. Run the installer and follow the wizard
3. Open pgAdmin from your Start Menu

### Step-by-Step: Connect pgAdmin to PostgreSQL

1. **Open pgAdmin** in your browser (`http://localhost:5050`)
2. Log in with the credentials you set:
   - Email: `admin@example.com`
   - Password: `admin123`

3. **Register a New Server:**
   - Right-click **Servers** in the left panel → **Register** → **Server...**

4. **General tab:**

   | Field | Value |
   |-------|-------|
   | Name | `Student API DB` |

5. **Connection tab:**

   | Field | Value |
   |-------|-------|
   | Host name / address | `student-api-db` *(if pgAdmin is in Docker)*<br>or `localhost` *(if pgAdmin is installed natively)* |
   | Port | `5432` |
   | Maintenance database | `student_api_db` |
   | Username | `student_api` |
   | Password | `student_api` |
   | Save password? | ✅ Yes |

6. Click **Save**

> **Important:** If pgAdmin runs in Docker, use the **container name**
> (`student-api-db`) as the host because both containers share the `student-net`
> network. If pgAdmin is installed natively on your machine, use `localhost`.

7. You should now see `Student API DB` in the left panel. Expand it:
   ```
   Student API DB → Databases → student_api_db → Schemas → public → Tables
   ```
   The Tables folder will be empty — we'll create them next!

---

## 5. Part C — Create the Database Schema Manually

### Using pgAdmin Query Tool

1. In pgAdmin, expand **Student API DB → Databases → student_api_db**
2. Right-click `student_api_db` → **Query Tool**
3. Copy and paste the following SQL, then click **Execute (▶)**:

```sql
-- =============================================================
-- Enable UUID generation
-- =============================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================
-- 1. USERS TABLE
-- =============================================================
CREATE TABLE IF NOT EXISTS users (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username      VARCHAR(80)  NOT NULL UNIQUE,
    password_hash TEXT         NOT NULL,
    role          VARCHAR(20)  NOT NULL DEFAULT 'user',
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);

-- =============================================================
-- 2. STUDENTS TABLE
-- =============================================================
CREATE TABLE IF NOT EXISTS students (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(200) NOT NULL UNIQUE,
    course          VARCHAR(200) NOT NULL,
    enrollment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_students_email ON students (email);

-- =============================================================
-- 3. AUTO-UPDATE TRIGGER for updated_at
-- =============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_students_updated_at
    BEFORE UPDATE ON students
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

4. You should see: **"Query returned successfully"**

5. Refresh the Tables node:
   Right-click **Tables** → **Refresh**
   You should now see `students` and `users`.

### Using psql (Command Line Alternative)

```powershell
docker exec -it student-api-db psql -U student_api -d student_api_db
```

Then paste the same SQL above, or run the init script directly:

```powershell
docker cp database/init.sql student-api-db:/tmp/init.sql
docker exec -it student-api-db psql -U student_api -d student_api_db -f /tmp/init.sql
```

### Verify Tables Were Created

In pgAdmin Query Tool or `psql`:

```sql
-- List all tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

Expected output:
```
 table_name
-----------
 users
 students
```

### Inspect Table Structure

```sql
-- Describe the students table
\d students
```

Or in pgAdmin: click on the table → **Properties** tab.

---

## 6. Part D — Explore SQL Queries

Now that the tables exist, let's practice the queries the application uses.

### Insert Sample Data

```sql
-- Insert a test user (password: "TestPass123!")
-- NOTE: In production the app generates the hash. This is for learning only.
INSERT INTO users (id, username, password_hash, role) VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'demo_admin',
    'scrypt:32768:8:1$placeholder$hash',
    'admin'
);

-- Insert sample students
INSERT INTO students (id, first_name, last_name, email, course) VALUES
    (uuid_generate_v4(), 'Alice', 'Smith', 'alice@university.com', 'Computer Science'),
    (uuid_generate_v4(), 'Bob',   'Jones', 'bob@university.com',   'Mathematics'),
    (uuid_generate_v4(), 'Carol', 'Lee',   'carol@university.com', 'Physics');
```

### Read Data (SELECT)

```sql
-- Get all students
SELECT id, first_name, last_name, email, course, enrollment_date, is_active
FROM students
ORDER BY created_at DESC;

-- Get a specific student by email
SELECT * FROM students WHERE email = 'alice@university.com';

-- Get only active students
SELECT first_name, last_name, course
FROM students
WHERE is_active = TRUE
ORDER BY last_name;

-- Count students per course
SELECT course, COUNT(*) as student_count
FROM students
GROUP BY course
ORDER BY student_count DESC;

-- Search students by name (case-insensitive partial match)
SELECT first_name, last_name, email
FROM students
WHERE first_name ILIKE '%ali%'
   OR last_name  ILIKE '%ali%';
```

### Update Data

```sql
-- Update a student's course
UPDATE students
SET course = 'Data Science'
WHERE email = 'alice@university.com'
RETURNING id, first_name, last_name, course, updated_at;

-- Deactivate a student
UPDATE students
SET is_active = FALSE
WHERE email = 'bob@university.com'
RETURNING id, first_name, is_active, updated_at;
```

### Delete Data

```sql
-- Delete a specific student
DELETE FROM students
WHERE email = 'carol@university.com';

-- Verify deletion
SELECT COUNT(*) FROM students;
```

### Pagination

```sql
-- Page 1 (first 10 results)
SELECT * FROM students ORDER BY created_at DESC LIMIT 10 OFFSET 0;

-- Page 2 (next 10 results)
SELECT * FROM students ORDER BY created_at DESC LIMIT 10 OFFSET 10;
```

### Clean Up Test Data

```sql
-- Remove all rows (keeps the tables)
TRUNCATE TABLE students RESTART IDENTITY CASCADE;
TRUNCATE TABLE users    RESTART IDENTITY CASCADE;
```

---

## 7. Part E — Deploy the Full Stack with Docker Compose

Now we deploy everything together: **PostgreSQL + Flask API** (and optionally
pgAdmin).

### Step 1 — Stop the Standalone Containers

If you still have containers running from Part A/B, stop them:

```powershell
docker stop student-api-db pgadmin
docker rm student-api-db pgadmin
docker network rm student-net
```

### Step 2 — Review the docker-compose.yml

The project already includes a `docker-compose.yml`. Here's what it does:

```yaml
version: "3.9"

services:
  # ---- PostgreSQL Database ----
  db:
    image: postgres:16-alpine
    container_name: student-api-db
    environment:
      POSTGRES_USER: student_api
      POSTGRES_PASSWORD: student_api
      POSTGRES_DB: student_api_db
    ports:
      - "5432:5432"
    volumes:
      - pg-data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro  # ← auto-runs on first start!
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U student_api -d student_api_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ---- Flask REST API ----
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: student-api
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=docker-secret-change-me
      - JWT_SECRET_KEY=docker-jwt-secret-change-me
      - DATABASE_URL=postgresql://student_api:student_api@db:5432/student_api_db
      - PORT=5000
    depends_on:
      db:
        condition: service_healthy   # ← waits for PostgreSQL to be ready
    restart: unless-stopped

volumes:
  pg-data:
```

**Key concepts:**
- `init.sql` is mounted into `/docker-entrypoint-initdb.d/` which PostgreSQL runs automatically on first start
- `depends_on: condition: service_healthy` ensures the API doesn't start until PostgreSQL passes its health check
- `DATABASE_URL` tells the Flask app how to connect to PostgreSQL
- The `db` service name becomes the hostname inside the Docker network

### Step 3 — (Optional) Add pgAdmin to docker-compose.yml

If you want pgAdmin as part of the stack, add this service:

```yaml
  # ---- pgAdmin (Optional GUI) ----
  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
```

### Step 4 — Build and Start Everything

```powershell
# Navigate to the project root
cd d:\KJC\DevOps\RestApiGithub

# Build images and start all services
docker compose up --build -d
```

### Step 5 — Watch the Logs

```powershell
# Follow all logs
docker compose logs -f

# Or follow only the API logs
docker compose logs -f api

# Or follow only the database logs
docker compose logs -f db
```

Wait until you see messages like:
```
student-api-db  | LOG:  database system is ready to accept connections
student-api     | [INFO] Listening at: http://0.0.0.0:5000
```

### Step 6 — Verify All Containers Are Running

```powershell
docker compose ps
```

Expected:
```
NAME             STATUS                   PORTS
student-api      Up (healthy)             0.0.0.0:5000->5000/tcp
student-api-db   Up (healthy)             0.0.0.0:5432->5432/tcp
```

### Step 7 — Test the Health Endpoint

```powershell
curl http://localhost:5000/api/v1/health
```

Expected response:
```json
{"status": "healthy"}
```

---

## 8. Part F — Test the API with cURL / Postman

### 8.1 Register a User

```powershell
curl -X POST http://localhost:5000/api/v1/auth/register `
    -H "Content-Type: application/json" `
    -d '{\"username\": \"testuser\", \"password\": \"SecurePass123!\"}'
```

Expected response (201):
```json
{
    "message": "User registered successfully",
    "user": {
        "id": "...",
        "username": "testuser",
        "role": "user"
    }
}
```

### 8.2 Login (Get JWT Token)

```powershell
curl -X POST http://localhost:5000/api/v1/auth/login `
    -H "Content-Type: application/json" `
    -d '{\"username\": \"testuser\", \"password\": \"SecurePass123!\"}'
```

Expected response (200):
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "user": { "id": "...", "username": "testuser", "role": "user" }
}
```

> **Copy the `access_token` value** — you need it for all student endpoints.

### 8.3 Create a Student

Replace `<TOKEN>` with your actual access token:

```powershell
curl -X POST http://localhost:5000/api/v1/students `
    -H "Content-Type: application/json" `
    -H "Authorization: Bearer <TOKEN>" `
    -d '{\"first_name\": \"Alice\", \"last_name\": \"Smith\", \"email\": \"alice@uni.com\", \"course\": \"Computer Science\"}'
```

### 8.4 List All Students

```powershell
curl http://localhost:5000/api/v1/students `
    -H "Authorization: Bearer <TOKEN>"
```

### 8.5 Get a Single Student

```powershell
curl http://localhost:5000/api/v1/students/<STUDENT_ID> `
    -H "Authorization: Bearer <TOKEN>"
```

### 8.6 Update a Student

```powershell
curl -X PUT http://localhost:5000/api/v1/students/<STUDENT_ID> `
    -H "Content-Type: application/json" `
    -H "Authorization: Bearer <TOKEN>" `
    -d '{\"course\": \"Data Science\"}'
```

### 8.7 Delete a Student

```powershell
curl -X DELETE http://localhost:5000/api/v1/students/<STUDENT_ID> `
    -H "Authorization: Bearer <TOKEN>"
```

### 8.8 Verify in pgAdmin

After running the API calls above, go to pgAdmin and run:

```sql
SELECT * FROM users;
SELECT * FROM students;
```

You should see the data that was created through the API!

---

## 9. Part G — Inspect & Debug

### Check Container Logs

```powershell
# API logs
docker logs student-api --tail 50

# Database logs
docker logs student-api-db --tail 50
```

### Open a Shell Inside the API Container

```powershell
docker exec -it student-api /bin/sh
```

### Open a psql Shell Inside the Database

```powershell
docker exec -it student-api-db psql -U student_api -d student_api_db
```

Then try:

```sql
-- Check what tables exist
\dt

-- See all students
SELECT * FROM students;

-- Check connection count
SELECT count(*) FROM pg_stat_activity WHERE datname = 'student_api_db';
```

### Check Docker Network

```powershell
docker network ls
docker network inspect restapigithub_default
```

### Check Volume Data

```powershell
docker volume ls
docker volume inspect restapigithub_pg-data
```

---

## 10. Part H — Clean Up

### Stop All Services (Keep Data)

```powershell
docker compose down
```

### Stop All Services AND Delete Data

```powershell
docker compose down -v
```

> **Warning:** `-v` removes the PostgreSQL data volume. All database content is lost!

### Remove Everything (Nuclear Option)

```powershell
docker compose down -v --rmi all
docker network prune -f
docker volume prune -f
```

---

## 11. Quick Reference — All Commands

| Task | Command |
|------|---------|
| Start everything | `docker compose up --build -d` |
| Stop everything | `docker compose down` |
| Stop + delete data | `docker compose down -v` |
| View logs | `docker compose logs -f` |
| View API logs only | `docker compose logs -f api` |
| Check status | `docker compose ps` |
| Rebuild after code changes | `docker compose up --build -d` |
| Open database shell | `docker exec -it student-api-db psql -U student_api -d student_api_db` |
| Open API container shell | `docker exec -it student-api /bin/sh` |
| Health check | `curl http://localhost:5000/api/v1/health` |

---

## 12. Troubleshooting

### "Port 5432 is already in use"

Another PostgreSQL instance is running on your machine.

```powershell
# Find what's using port 5432
netstat -ano | findstr :5432

# Option 1: Stop your local PostgreSQL service
net stop postgresql-x64-16

# Option 2: Change the port in docker-compose.yml
# ports: "5433:5432" (then connect to 5433 from your machine)
```

### "Connection refused" from the API

The API started before PostgreSQL was ready. The `depends_on` + health check
should prevent this, but if it happens:

```powershell
docker compose restart api
```

### pgAdmin Can't Connect to Database

| Scenario | Host to use |
|----------|-------------|
| pgAdmin in Docker (same network) | `student-api-db` or `db` |
| pgAdmin installed on your PC | `localhost` |

### "No such table" / Tables Missing

The init script only runs on the **first** container startup with an empty
volume. If you need to re-run it:

```powershell
# Remove the volume and restart
docker compose down -v
docker compose up --build -d
```

### API Returns 500 Errors

Check the logs:

```powershell
docker compose logs api --tail 100
```

Common causes:
- `DATABASE_URL` is wrong (check env vars in `docker-compose.yml`)
- Tables don't exist (run the init SQL manually)

---

## 13. Appendix — SQL Queries Cheat-Sheet

### Data Definition (DDL)

```sql
-- Create a table
CREATE TABLE IF NOT EXISTS students (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(200) NOT NULL UNIQUE,
    course          VARCHAR(200) NOT NULL,
    enrollment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add an index
CREATE INDEX idx_students_email ON students (email);

-- Drop a table
DROP TABLE IF EXISTS students CASCADE;

-- Add a new column
ALTER TABLE students ADD COLUMN gpa DECIMAL(3,2);

-- Remove a column
ALTER TABLE students DROP COLUMN gpa;
```

### Data Manipulation (DML)

```sql
-- INSERT
INSERT INTO students (id, first_name, last_name, email, course)
VALUES (uuid_generate_v4(), 'Alice', 'Smith', 'alice@uni.com', 'CS')
RETURNING *;

-- SELECT with filter
SELECT * FROM students WHERE is_active = TRUE ORDER BY last_name;

-- SELECT with LIKE (case-insensitive)
SELECT * FROM students WHERE first_name ILIKE '%ali%';

-- SELECT with pagination
SELECT * FROM students ORDER BY created_at DESC LIMIT 10 OFFSET 0;

-- UPDATE
UPDATE students SET course = 'Data Science' WHERE email = 'alice@uni.com'
RETURNING id, first_name, course, updated_at;

-- DELETE
DELETE FROM students WHERE id = 'some-uuid-here';

-- COUNT
SELECT COUNT(*) FROM students;

-- GROUP BY
SELECT course, COUNT(*) FROM students GROUP BY course;
```

### Utility Commands (psql)

```sql
-- List all databases
\l

-- Connect to a database
\c student_api_db

-- List all tables
\dt

-- Describe a table
\d students

-- Show all indexes
\di

-- Exit psql
\q
```

---

## Summary — What You Learned

| Topic | What You Did |
|-------|-------------|
| **Docker** | Pulled images, created networks, ran containers, used volumes |
| **PostgreSQL** | Created databases, tables, indexes, and triggers |
| **pgAdmin** | Connected to a database, ran queries, inspected data |
| **SQL** | Wrote DDL (CREATE TABLE) and DML (INSERT, SELECT, UPDATE, DELETE) |
| **Docker Compose** | Orchestrated multi-container applications with health checks |
| **REST API** | Tested CRUD endpoints with JWT authentication |
| **Networking** | Understood container-to-container communication |
| **Environment Variables** | Configured apps via env vars (DATABASE_URL, secrets) |

---

*Happy Learning! 🚀*
