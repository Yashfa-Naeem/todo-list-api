# Todo List RESTful API

Internship project - A complete task management API built with FastAPI and PostgreSQL.

## Features
- **Authentication:** JWT tokens, OAuth 2.0 (Google), Email verification, Password reset
- **Task Management:** Complete CRUD operations with user isolation
- **File Handling:** Upload and download file attachments
- **Analytics:** 5 report endpoints (task counts, averages, trends, overdue tracking)
- **Algorithms:** Similar tasks finder using word comparison
- **Logging:** Request logging middleware

## Technologies Used
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, SQLAlchemy ORM
- **Authentication:** JWT, OAuth 2.0, bcrypt
- **Tools:** Git, Postman, Pydantic
- **Other:** SMTP email, session middleware

## Project Structure
```
todo/
├── api/              # Application modules
│   ├── auth/         # Authentication (signup, login, OAuth)
│   ├── tasks/        # Task CRUD operations
│   ├── reports/      # Analytics endpoints
│   ├── database/     # Database config and models
│   └── middleware/   # Logging middleware
├── app/              # Main application
├── tests/            # Test files
└── uploads/          # File storage
```

## Setup Instructions
1. Clone the repository
2. Install dependencies: `uv sync`
3. Configure `.env` file with database credentials
4. Run server: `uv run uvicorn app.main:app --reload`

## API Endpoints
- **Auth:** `/api/auth/signup`, `/api/auth/login`, `/api/auth/google/login`
- **Tasks:** `/api/tasks/` (CRUD operations)
- **Files:** `/api/tasks/{id}/attachments`
- **Reports:** `/api/reports/task-counts`, `/api/reports/average-completed-per-day`
