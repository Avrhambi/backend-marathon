import time
import redis
from celery import Celery

app = Celery("tasks", broker="amqp://guest:guest@localhost:5672//")
redis_client = redis.Redis(host="localhost", port=6379, db=0)

@app.task
def process_payment(idempotency_key: str, user_id: str, amount: float):
    # TODO: Implement idempotency check (If the network drops and Celery retries, this runs twice!)
    cache_key = f"idempotency:{idempotency_key}"

    # 1. CHECK IF ALREADY PROCESSED
    if redis_client.get(cache_key):
        print(f"⏩ [SKIPPED] Task {idempotency_key} already processed.")
        return {"status": "SKIPPED_DUPLICATE", "idempotency_key": idempotency_key}

    # 2. RUN BUSINESS LOGIC
    print(f"🔄 [PROCESSING] Payment of ${amount} for user {user_id}...")
    time.sleep(1)

    # 3. LOCK KEY WITH 24-HOUR EXPIRATION
    redis_client.set(cache_key, "COMPLETED", ex=86400)

    # TODO: Implement cache saving with expiration
    return {"status": "SUCCESS", "idempotency_key": idempotency_key}