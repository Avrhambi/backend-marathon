import asyncio

async def worker_internal_catch():
    # TODO: Wrap the task logic in an internal try...except block
    # TODO: Simulate an error (raise RuntimeError("Database connection lost")) and log it
    try:
        print("Worker started...")
        await asyncio.sleep(1)
        raise RuntimeError("Database connection lost")
    except RuntimeError as e:
        print(f"Error occurred: {e}")

async def main_task_3a():
    task = asyncio.create_task(worker_internal_catch())
    await asyncio.sleep(1)
    await task
    print("Main task completed.")

if __name__ == "__main__":
    asyncio.run(main_task_3a())

    