# Day 2: PostgreSQL Interactive Course

## Goals
- Understand database schemas, indexing, and table relationships.
- Benchmark database queries to understand the performance impact of indexing and query structures.
- Setup a reproducible Postgres environment.

---

## Part 1: PostgreSQL Setup and Benchmarking

### 1. Database Setup (`setup.ps1` & `schema.sql`)
**Assignment:** Initialize a local PostgreSQL instance and provision it with a schema.
**Solution & Logic:** Use the provided PowerShell script `setup.ps1` to start a PostgreSQL docker container or initialize the local DB. Then, run `schema.sql` to construct the tables.
**Mechanics:** `schema.sql` defines the Data Definition Language (DDL) for creating the entities, ensuring strict typing, constraints, and relational integrity via foreign keys.

### 2. Running Benchmarks (`run_benchmarks.sql`)
**Assignment:** Execute a series of SQL queries to measure read and write performance before and after optimization.
**Solution & Logic:** The script uses `EXPLAIN ANALYZE` alongside large `INSERT` and `SELECT` operations.
**Mechanics:**
- `EXPLAIN ANALYZE` executes the query and provides real run-time statistics.
- **Without Indexes:** The database performs Sequential Scans, which degrade in performance as the table grows.
- **With Indexes:** The database performs Index Scans or Bitmap Index Scans, drastically reducing lookup times for specific queries but adding a slight overhead to `INSERT`/`UPDATE` operations due to index maintenance.

---
*Run these SQL scripts interactively using a Database Client (like pgAdmin or DBeaver) or through the `psql` CLI to see real-time query plans and execution times.*
