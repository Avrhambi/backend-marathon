import asyncio
import time

def heavy_cpu_calculation(n: int) -> int:
    """Blocking CPU-Bound function"""
    print(f"Starting heavy calculation for {n}...")
    count = 0
    for i in range(n):
        count += i
    print("Finished heavy calculation!")
    return count

async def heartbeat():
    """Background heartbeat task that should run every 0.5s without interruption, total 3 seconds"""
    for _ in range(6):
        print("Heartbeat tick...")
        await asyncio.sleep(0.5)

async def main_task_2():
    # # TODO: Run heartbeat concurrently alongside the heavy calculation
    # # TODO: Use asyncio.to_thread for heavy_cpu_calculation to avoid blocking the Event Loop
    n = 10
    start_time = time.perf_counter()
    await asyncio.gather(
        heartbeat(),
        asyncio.to_thread(heavy_cpu_calculation, n)
    )       
    print(f"Total time taken using asyncio.gather, n={n}: {time.perf_counter() - start_time:.3f} seconds\n")
    


if __name__ == "__main__":
    asyncio.run(main_task_2())