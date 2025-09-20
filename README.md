# Visitor Management System - Backend

This is a backend implementation of a **Visitor Management System** built with **FastAPI**, **MySQL**, and **SQLAlchemy**. The system allows residents and security personnel in a society to manage visitors effectively, with support for **temporary** and **recurring visitors**, check-ins, check-outs, and approvals.

---

## Table of Contents

1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Setup Instructions](#setup-instructions)
5. [API Endpoints](#api-endpoints)
6. [Authentication](#authentication)
7. [Database Models](#database-models)
8. [Running the Project](#running-the-project)

---

## Features

* Resident and Security roles with role-based authentication
* Resident can invite visitors (temporary or recurring)
* Security can check visitors in and out
* Approval workflow: Residents approve or deny visitor requests
* Detailed visitor logs with check-in and check-out timestamps
* JWT authentication for secure API access

---

## Technology Stack

* **Python 3.11**
* **FastAPI** – backend framework
* **MySQL** – relational database
* **SQLAlchemy** – ORM for database models
* **Pydantic** – request/response validation
* **Uvicorn** – ASGI server
* **Docker** (optional) – for containerization in production
* **JWT** – authentication and authorization

---

## Project Structure

```
visitor-management/
│── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── config.py            # Config for DB, JWT secret, settings
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── visitor.py
│   │   └── visit.py
│   ├── schemas/             # Pydantic models
│   ├── routes/              # API routers
│   ├── services/            # Business logic
│   ├── utils/               # Helpers (JWT, security, dependencies)
│   ├── database.py          # SQLAlchemy session/engine
│── migrations/              # Alembic migrations (optional)
│── tests/                   # Unit tests
│── requirements.txt
│── README.md
│── Dockerfile               # For deployment
│── docker-compose.yml       # For deployment
```

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone <repo-url>
cd visitor-management
```

2. **Create a virtual environment and activate it**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure MySQL database**

* Create a database in MySQL:

```sql
CREATE DATABASE visitor_mgmt;
```

* Update `app/config.py` with your database credentials:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "visitor_mgmt"
```

5. **Create tables**

* Either use Alembic migrations or SQLAlchemy:

```python
from app.database import Base, engine
Base.metadata.create_all(bind=engine)
```

---

## API Endpoints

### Authentication

* `POST /auth/register` – Register resident or security
* `POST /auth/login` – Login and get JWT access token

### Visitor Management (Resident)

* `POST /visitors/` – Create a visitor (automatic pending visit)
* `GET /visits/resident/visitors` – List all visitors for this resident
* `POST /visits/approve/{visit_id}` – Approve a visitor visit
* `POST /visits/deny/{visit_id}` – Deny a visitor visit

### Visitor Management (Security)

* `GET /visits/security/visits` – List all visits for security
* `POST /visits/checkin/{visit_id}` – Mark check-in
* `POST /visits/checkout/{visit_id}` – Mark check-out

---

## Authentication

* JWT authentication is used for all endpoints
* Residents must provide **phone** and optionally **email**
* Security can log in with **phone** only
* Include JWT in `Authorization` header for protected routes:

```
Authorization: Bearer <access_token>
```

---

## Database Models

### User

* `id`, `name`, `phone`, `email`, `password_hash`, `role` (RESIDENT/SECURITY)

### Visitor

* `id`, `name`, `phone`, `visitor_type` (TEMPORARY/RECURRING), `resident_id`

### Visit

* `id`, `visitor_id`, `resident_id`, `security_id`, `check_in`, `check_out`, `status` (PENDING/APPROVED/DENIED/CHECKED\_IN/CHECKED\_OUT)

---

## Running the Project

```bash
uvicorn app.main:app --reload
```

* API runs at: `http://127.0.0.1:8000`
* Use Postman or curl to test endpoints
* Include JWT token in requests for protected routes
