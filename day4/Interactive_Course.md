# Day 4: Message Brokers (RabbitMQ & Kafka) Interactive Course

## Goals
- Understand the role of message brokers in distributed systems.
- Differentiate between RabbitMQ (message queue) and Kafka (event streaming).
- Implement asynchronous messaging and event-driven architecture using Python.

---

## Part 1: RabbitMQ & Kafka Integration (`rabbit-kafka/`)

### 1. Environment Setup
**Assignment:** Configure local instances of RabbitMQ and Kafka.
**Solution & Logic:** Use Docker Compose or provided scripts to spin up RabbitMQ (with management plugin) and Kafka (with Zookeeper or KRaft).

### 2. Message Queueing with RabbitMQ
**Assignment:** Write a producer that sends tasks to a queue and a consumer/worker that processes them asynchronously (e.g., using Celery or Pika).
**Mechanics:**
- **Producer:** Connects to RabbitMQ exchange/queue and publishes messages.
- **Consumer:** Listens to the queue and acknowledges (`ack`) messages only after successful processing. This guarantees at-least-once delivery.
- **Use Case:** Task distribution, point-to-point messaging, and delayed execution.

### 3. Event Streaming with Kafka
**Assignment:** Write a producer that publishes events to a Kafka topic and a consumer group that reads the stream.
**Mechanics:**
- **Topics & Partitions:** Kafka stores ordered events durably in partitions.
- **Consumer Groups:** Consumers read from partitions. Kafka keeps track of offsets, allowing consumers to replay events or catch up if they go offline.
- **Use Case:** High-throughput telemetry, log aggregation, event sourcing, and real-time analytics.

---
*To run this interactively, activate the virtual environment (`.venv/Scripts/activate`), ensure your brokers are running, and execute the producer and consumer scripts in separate terminal windows to observe message passing in real-time.*
