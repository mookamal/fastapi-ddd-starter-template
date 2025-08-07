# 🏗️ FastAPI Clean Architecture Starter Template

A production-ready FastAPI starter with full support for:

- Clean DDD architecture (Domain-Driven Design)
- Async SQLAlchemy 2.0 + Alembic
- User authentication with JWT
- Secure password hashing with Bcrypt
- Environment-based config using Pydantic v2
- Custom exception handling
- Modular, testable, extensible project structure

---

## 🚀 Key Features

### ✅ Clean DDD Architecture

- **Domain Layer**: Entities, repository interfaces, domain services
- **Application Layer**: DTOs and application-level services
- **Infrastructure Layer**: Database models, concrete repositories, JWT utils
- **API Layer**: FastAPI routes and dependency injection

### ✅ Async/Await First

All database calls and endpoints use async/await with full support for asyncpg.

### ✅ User Management

- User entity with fields: `id`, `name`, `email`, `password_hash`, `is_active`, `created_at`
- Registration and login with JWT tokens
- Password hashing using `passlib[bcrypt]`
- Email validation via Pydantic

### ✅ Security

- JWT token authentication
- Bcrypt password hashing
- Dependency-injected authorization checks

### ✅ Configuration

- Environment-based using `pydantic-settings`
- Centralized config via `.env`

### ✅ Error Handling

- Custom exception classes
- Global error handlers with proper HTTP status codes

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mookamal/fastapi-ddd-template.git
cd fastapi-ddd-template
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/scriptor_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run Alembic migrations

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 5. Start the development server

```bash
uvicorn app.main:app --reload
```

---

## 🔑 API Endpoints

| Method | Endpoint               | Description             |
|--------|------------------------|-------------------------|
| POST   | /api/v1/auth/register  | Register a new user     |
| POST   | /api/v1/auth/login     | Login and get JWT token |
| GET    | /api/v1/auth/me        | Get current user (protected) |
| GET    | /docs                  | Swagger API Documentation |

---

## 🧪 Coming Soon (optional)

- ✅ Pytest + Test Client setup  
- ✅ Dockerfile and docker-compose support  
- ✅ CI/CD example (GitHub Actions)  
- ✅ Role-based access control (RBAC)  

---

## 🧱 Tech Stack

- FastAPI
- SQLAlchemy 2.0 (async ORM)
- PostgreSQL
- Alembic
- Pydantic v2
- Passlib / Bcrypt
- Python-Jose
- Docker (optional)

---

## 🧼 Project Structure

```
app/
├── api/                  # FastAPI routes
│   └── v1/
├── application/          # DTOs and application logic
├── domain/               # Entities and interfaces
├── infrastructure/       # DB models, JWT utils, repositories
├── config/                 # Config, security, and utils
├── main.py               # FastAPI app entry point
```

---

## 🪪 License

MIT License © [Your Name or Organization]

---

## 🛠️ Contribution

This template is designed to be extended and improved.  
Feel free to fork and customize for your next SaaS, microservice, or platform backend.

---

Made with ❤️ by Mohamed Kamal