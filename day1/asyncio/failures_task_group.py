import asyncio

async def failing_task():
    await asyncio.sleep(0.1)
    raise ValueError("Invalid payload")

async def main_task_3c():
    # TODO: Use async with asyncio.TaskGroup() as tg:
    # TODO: Catch the exception outside the TaskGroup using except* ValueError
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(failing_task())
            tg.create_task(asyncio.sleep(1))
    except* ValueError as e:
        for exc in e.exceptions:
            print(f"Caught Error in background tasks: {type(exc).__name__} {exc}")

    print("Main task completed.")

if __name__ == "__main__":
    asyncio.run(main_task_3c())