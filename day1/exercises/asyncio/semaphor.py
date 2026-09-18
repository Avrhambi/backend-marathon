import asyncio
import time

async def fetch_item(item_id: int, sem: asyncio.Semaphore):
    # TODO: Wrap the logic in the Semaphore to limit concurrency to 5 requests at a time
    async with sem:
        print(f"[{time.strftime('%X')}] Starting fetch {item_id}, {sem}")
        await asyncio.sleep(1)  # I/O Simulation
        print(f"[{time.strftime('%X')}] Finished fetch {item_id}, {sem}")
        return f"Data {item_id}"
    
async def main_task_1():
    # TODO: Create a Semaphore with a limit of 5
    start_time = time.perf_counter()
    sem = asyncio.Semaphore(5)
    # TODO: Create a list of 100 tasks and run them concurrently using asyncio.gather
    tasks = [fetch_item(i, sem) for i in range(100)]
    await asyncio.gather(*tasks)
    print(f"Total time taken using asyncio.gather: {time.perf_counter() - start_time:.2f} seconds")                 


if __name__ == "__main__":
    asyncio.run(main_task_1())