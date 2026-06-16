# Task Manager API

A beginner-friendly FastAPI project for managing tasks with PostgreSQL, JWT authentication, password hashing, and role-based authorization.

## Overview

This project uses a clean layered architecture so each part of the application has one clear responsibility:

- Routers handle HTTP requests and responses.
- Services contain business rules.
- Repositories contain database queries.
- Models define SQLAlchemy database tables.
- Schemas define Pydantic request and response shapes.
- Auth dependencies protect routes and check user roles.

Tables are created automatically with `Base.metadata.create_all()` for beginner simplicity. Alembic migrations are intentionally not included.

## Features

- User registration
- User login with JWT access tokens
- Password hashing with bcrypt
- Get current logged-in user
- Task create, read, update, and delete
- Normal users can only manage their own tasks
- Admin users can view all users and all tasks
- Environment-based PostgreSQL configuration

## Tech Stack

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- psycopg2-binary
- Pydantic
- python-jose for JWT
- Passlib bcrypt
- Python-dotenv
- Uvicorn

## Folder Structure

```text
task_manager_api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── auth.py
│   │   └── task.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── task_repository.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── task_service.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── admin.py
│   └── auth/
│       ├── security.py
│       └── dependencies.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## PostgreSQL Setup

Install PostgreSQL locally and make sure the PostgreSQL server is running.

### Create Database Manually With pgAdmin

1. Open pgAdmin.
2. Connect to your PostgreSQL server.
3. Right-click `Databases`.
4. Choose `Create` then `Database`.
5. Enter `task_manager_db` as the database name.
6. Click `Save`.

### Create Database Manually With psql

```bash
psql -U postgres
```

Then run:

```sql
CREATE DATABASE task_manager_db;
```

Exit psql:

```sql
\q
```

## Create Virtual Environment

From inside the `task_manager_api` folder:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Create `.env`

Copy `.env.example` to `.env`.

Windows PowerShell:

```bash
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

## Add PostgreSQL Credentials

Open `.env` and update the values for your local PostgreSQL setup:

```env
DATABASE_URL=postgresql://postgres:your_real_password@localhost:5432/task_manager_db
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit `.env`. It is ignored by `.gitignore`.

## Run Server

From inside the `task_manager_api` folder:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Tasks

- `POST /api/v1/tasks/`
- `GET /api/v1/tasks/`
- `GET /api/v1/tasks/{task_id}`
- `PUT /api/v1/tasks/{task_id}`
- `DELETE /api/v1/tasks/{task_id}`

### Admin

- `GET /api/v1/admin/users`
- `GET /api/v1/admin/tasks`

## Authentication Flow

1. Register a user with `POST /api/v1/auth/register`.
2. Log in with `POST /api/v1/auth/login`.
3. Copy the returned `access_token`.
4. Send the token as a bearer token for protected routes.

Example header:

```text
Authorization: Bearer your_access_token
```

## Authorization Flow

New registered users receive the `user` role by default.

- Users with role `user` can manage only their own tasks.
- Users with role `admin` can access admin routes.

For this beginner version, make a user an admin manually in PostgreSQL:

```sql
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

Then log in again to receive a fresh JWT.

## Swagger UI Testing Flow

1. Start the server with `uvicorn app.main:app --reload`.
2. Open `http://127.0.0.1:8000/docs`.
3. Use `POST /api/v1/auth/register` to create an account.
4. Use `POST /api/v1/auth/login` to get an access token.
5. Click `Authorize` at the top of Swagger UI.
6. Paste only the token value into the bearer token field.
7. Test `GET /api/v1/auth/me`.
8. Create and manage tasks using the `/api/v1/tasks/` endpoints.
9. To test admin endpoints, update the user's role to `admin` in PostgreSQL and log in again.

## Future Improvements

- Add Alembic migrations
- Add refresh tokens
- Add email verification
- Add pagination and filtering
- Add automated tests
- Add Docker support
- Add stronger password validation

![alt text](<Screenshot 2026-06-16 181502.png>)

![alt text](<Screenshot 2026-06-16 181604.png>)

![alt text](<Screenshot 2026-06-16 181650.png>)

![alt text](<Screenshot 2026-06-16 181725.png>)

![alt text](<Screenshot 2026-06-16 181804.png>)
