# Day 1: AsyncIO & Pydantic Interactive Course

## Goals
- Understand and apply Python's `asyncio` for concurrent programming.
- Handle failures and task groups in async environments.
- Master data validation and serialization using `pydantic`.

---

## Part 1: AsyncIO

### 1. CPU Bound Operations (`cpu_bound.py`)
**Assignment:** Run a heartbeat task concurrently alongside a heavy calculation, avoiding blocking the Event Loop.
**Solution & Logic:** Use `asyncio.gather()` to run multiple awaitables concurrently. For the heavy CPU calculation, use `asyncio.to_thread()` to run it in a separate thread, preventing it from blocking the main async event loop.
**Mechanics:** `asyncio.to_thread()` delegates the blocking operation to a thread pool. The event loop remains responsive and can print the "Heartbeat tick".

### 2. Failure Handling
**Assignment:** Handle failures in async tasks using callbacks, internal handling, and task groups (`failures_callaback.py`, `failures_internal_handling.py`, `failures_task_group.py`).
**Solution & Logic:**
- **Internal Handling:** Wrap the `await` calls in `try/except` blocks inside the async function.
- **Callbacks:** Use `task.add_done_callback()` to handle the result or exception when a task finishes.
- **Task Groups:** Use `asyncio.TaskGroup()` (Python 3.11+) as an async context manager to spawn sub-tasks. If any task fails, the group cancels the remaining tasks and raises an `ExceptionGroup`.

### 3. Semaphores (`semaphor.py`)
**Assignment:** Limit the number of concurrent async tasks.
**Solution & Logic:** Use `asyncio.Semaphore(value)`.
**Mechanics:** Wrap the critical section of the async function with `async with semaphore:`. This ensures that only `value` number of tasks can execute the block concurrently, preventing resource exhaustion.

---

## Part 2: Pydantic

### 1. Basic Validation (`basic_validation.py`)
**Assignment:** Define a `Product` model with `id` (int), `name` (str), `price` (float), and `is_available` (bool).
**Solution & Logic:** Create a class inheriting from `BaseModel`. Pydantic will automatically coerce strings like `"101"` to integers and `"99.99"` to floats during parsing.

### 2. Medium & Complex Validation (`medium_validation.py`, `complex_validation.py`)
**Assignment:** Implement complex validation rules (e.g., custom validators, nested models).
**Solution & Logic:** Use `@field_validator` and `@model_validator` to enforce custom business logic. Use nested Pydantic models to validate hierarchical JSON payloads.

---
*Run these exercises interactively using your Python IDE or Jupyter Notebook by loading the code snippets from the `exercises/` folder!*
