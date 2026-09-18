import asyncio

background_tasks = set()

def handle_result(task: asyncio.Task):
    # TODO: Remove the task from background_tasks
    background_tasks.discard(task)
    # TODO: Retrieve the result using task.result() and catch the exception
    try:
        result = task.result()
        print(f"Task completed successfully with result: {result}")
    except Exception as e:
        print(f"Task raised an exception: {e}")

async def failing_worker():
    await asyncio.sleep(0.2)
    raise RuntimeError("Background worker crashed!")

async def main_task_3b():
    # TODO: Create a Task, add it to the strong reference set, and register add_done_callback
    task = asyncio.create_task(failing_worker())
    background_tasks.add(task)
    task.add_done_callback(handle_result)

    await asyncio.sleep(1)  # Wait for the background task to complete
    print("Main task completed.")
    

if __name__ == "__main__":
    asyncio.run(main_task_3b())