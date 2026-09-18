# Day 3: API Design & Clean FastAPI Interactive Course

## Goals
- Learn API design best practices and RESTful conventions.
- Build a structured and clean FastAPI application.
- Integrate SQLAlchemy for ORM-based database interactions.

---

## Part 1: API Design (`api-design/`)

### Design Questions & Solutions
**Assignment:** Given a set of requirements in `questions.docx`, design the corresponding API endpoints.
**Solution & Logic:** The answers are provided in `solutions.docx`.
**Mechanics:**
- **Resource Naming:** Use plural nouns for endpoints (e.g., `/users`, `/orders`).
- **HTTP Methods:** Use `GET` for retrieval, `POST` for creation, `PUT`/`PATCH` for updates, and `DELETE` for removal.
- **Status Codes:** Return 200 OK, 201 Created, 400 Bad Request, 404 Not Found, etc., to accurately represent the outcome of the API call.

---

## Part 2: Clean FastAPI with SQLAlchemy (`clean-fastapi-sqlachemy/`)

### Application Structure
**Assignment:** Build a FastAPI backend implementing Clean Architecture principles, separating routing, business logic, and database access.
**Solution & Logic:**
- **`app/api/` (Routers & Dependencies):** Defines the FastAPI endpoints and dependency injection (e.g., getting the database session).
- **`app/schemas/` (Pydantic Models):** Defines the input/output data shapes and validation.
- **`app/services/` (Business Logic):** Contains the core logic, isolated from HTTP details.
- **`app/database/` (SQLAlchemy Setup):** Handles connection pooling, session creation, and declarative base definitions.
- **`app/models/` (SQLAlchemy Models):** Maps Python classes to database tables.

### Mechanics & Flow
1. A client sends a request to a route defined in `routers.py`.
2. FastAPI uses dependencies (`Depends()`) to inject a database session.
3. FastAPI parses and validates the incoming JSON against a Pydantic schema.
4. The router calls a function in the `services/` layer.
5. The service executes business logic and uses SQLAlchemy models to interact with the DB.
6. Data is returned through a Pydantic response schema, automatically serializing objects to JSON.

---
*To run this code interactively, use the provided `.venv` or create your own, install dependencies, and run `uvicorn app.main:app --reload`. Explore the interactive Swagger UI at `http://127.0.0.1:8000/docs`.*
