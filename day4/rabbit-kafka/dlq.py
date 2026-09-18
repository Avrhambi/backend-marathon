from celery import Celery
import celery
from kombu import Exchange, Queue


app =  Celery("tasks", broker="amqp://guest:guest@localhost:5672//")

# 1. SETUP DLQ TOPOLOGY
default_exchange = Exchange("default", type="direct")
dlx_exchange = Exchange("dlx", type="direct")

app.conf.task_queues = (
    Queue(
        "default",
        exchange=default_exchange,
        routing_key="default",
        queue_arguments={
            "x-dead-letter-exchange": "dlx",  # Redirect failed tasks here
            "x-dead-letter-routing-key": "dlq",
        },
    ),
    Queue("dlq", exchange=dlx_exchange, routing_key="dlq"), # Isolated poison-pill queue
)

class PermanentFailure(Exception):
    """Custom exception that bypasses retries."""
    pass


@app.task(bind=True, max_retries=3)
def process_strict_payment(self, idempotency_key: str, amount: float):
    # TODO: implement a validation checks that trigger a task move to dlq  (A negative amount will fail all 3 retries and waste CPU cycles)
    # --- CHECK 1: PERMANENT FAILURE --
    if amount <= 0:
        print(f"⛔ [DLQ ROUTE] Invalid amount ${amount}. Routing to DLQ.")
        raise ValueError("Invalid amount") 

    # --- CHECK 2: CORE LOGIC & RETRIES ---
    try:
        print(f"Processing ${amount}...")
        return {"status": "SUCCESS"}
    except Exception as exc:
        if self.request.retries >= self.max_retries:
            print(f"💥 [EXHAUSTED] Max retries hit. Routing to DLQ.")
            raise exc
    # Explicit retry trigger
    raise self.retry(exc=exc, countdown=2 ** self.request.retries)