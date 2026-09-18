# Day 5: CI/CD & Debugging Interactive Course

## Goals
- Automate testing and deployment using Continuous Integration / Continuous Deployment (CI/CD) pipelines.
- Containerize backend applications using Docker.
- Master advanced debugging techniques for complex backend issues.

---

## Part 1: CI/CD Pipeline (`ci-cd/`)

### 1. Dockerization
**Assignment:** Containerize the FastAPI application using Docker.
**Solution & Logic:** The `Dockerfile` defines the environment.
**Mechanics:**
- It starts from a lightweight Python base image (`python:3.10-slim`).
- Copies requirements and installs dependencies.
- Copies the application code.
- Exposes the application port and defines the entrypoint (e.g., `uvicorn`).

### 2. GitHub Actions (`.github/workflows/ci.yml`)
**Assignment:** Set up a CI pipeline that runs tests automatically on every push.
**Solution & Logic:** The `ci.yml` file configures the GitHub Actions runner.
**Mechanics:**
- **Triggers:** The workflow runs on `push` or `pull_request` to the main branch.
- **Jobs:** Sets up Python, installs dependencies from `requirements-dev.txt`, runs the linter (like flake8 or black), and executes tests using `pytest`.
- **Validation:** If any test fails, the pipeline fails, preventing broken code from merging.

---

## Part 2: Debugging (`debugging/`)

### Advanced Debugging Techniques
**Assignment:** Resolve the issues described in `metadata.txt`.
**Solution & Logic & Mechanics:**
- **Logging:** Ensure the application emits structured logs with proper levels (INFO, ERROR, DEBUG). Trace IDs help correlate logs across distributed services.
- **Interactive Debuggers:** Use `pdb` or IDE debuggers (like VS Code or PyCharm) to set breakpoints, step through code, and inspect the runtime state of variables.
- **Exception Handling:** Read full tracebacks carefully from the bottom up to locate the exact origin of the error.

---
*To experience this interactively, run `pytest` locally inside the `ci-cd` folder to see the tests pass/fail. You can also build and run the Docker container locally using `docker build -t myapp .` and `docker run -p 8000:8000 myapp`.*
