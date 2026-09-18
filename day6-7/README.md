# Days 6-7: Final Project - Async Report Engine

## Goals
- Combine all learned concepts: FastAPI, PostgreSQL, message brokers (RabbitMQ/Kafka), and async processing.
- Build a robust, distributed background task processing engine.
- Apply clean code architecture and advanced testing strategies.

---

## The Assignment Requirements

You are tasked with building a full-stack **Async Report Engine**. The system will accept requests to generate heavy reports (e.g., CSV exports of user analytics) and process them in the background without blocking the main API.

### Core Requirements:
1. **API Layer (FastAPI):**
   - `POST /reports`: Accepts a request to generate a report. Returns a `task_id` and a 202 Accepted status immediately.
   - `GET /reports/{task_id}`: Returns the current status of the report (e.g., `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`).
   - `GET /reports/{task_id}/download`: Allows downloading the generated report if the status is `COMPLETED`.

2. **Message Broker Integration:**
   - Once the API receives a report request, it must publish a message to a RabbitMQ queue (or Kafka topic).

3. **Background Worker:**
   - A separate worker process (e.g., a Celery worker or a custom async consumer) listens to the queue.
   - Upon receiving a task, it simulates a long-running CPU-bound process (or actually queries the DB and generates a CSV).
   - It updates the task's status in the PostgreSQL database.

4. **Database (PostgreSQL):**
   - Store report metadata (task ID, status, creation time, completion time, file path).

### Architecture Reference
This final project is built as a separate, fully standalone application repository to simulate a real-world microservice architecture.

**Reference:** The full codebase and detailed documentation for this assignment can be found in its dedicated public repository: [Avrhambi/async-report-engine](https://github.com/Avrhambi/async-report-engine).

---
*Run this project interactively by following the `README.md` on the repository linked above. You will typically need to run `docker-compose up` to spin up the API, the Worker, PostgreSQL, and RabbitMQ simultaneously.*
