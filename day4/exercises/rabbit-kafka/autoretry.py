import random
import redis
from celery import Celery

app = Celery("tasks", broker="amqp://guest:guest@localhost:5672//")
redis_client = redis.Redis(host="localhost", port=6379, db=0)

@app.task(
    bind=True,
    max_retries=3,
    autoretry_for=(ConnectionError, TimeoutError), # Auto-catch network bugs
    retry_backoff=True,                             # 2s, 4s, 8s exponential wait
    retry_backoff_max=600,                          # Max wait 10 min
    retry_jitter=True                               # Randomize backoff delay slightly
)

@app.task
def process_payment_with_retry(self, idempotency_key: str, user_id: str, amount: float):
    # TODO: Implement auto-retry with exponential backoff (If network drops, task dies immediately)
    cache_key = f"idempotency:{idempotency_key}"

    if redis_client.get(cache_key):
        return {"status": "SKIPPED_DUPLICATE"}

    if random.random() < 0.7:
        print(f"⚠️ Network error! Retry attempt {self.request.retries + 1}/3...")
        raise ConnectionError("Gateway Timeout")

    print(f"Payment successful for {user_id}")
    return {"status": "SUCCESS"}