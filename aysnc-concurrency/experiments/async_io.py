import asyncio
import time
from tqdm.asyncio import tqdm

async def task(task_id: int):
    await asyncio.sleep(0.1)
    if task_id == 500:
        raise ValueError(f"Task {task_id} encountered an error")
    return f"Task {task_id} completed"

async def main():
    start = time.time()
    # Create and gather tasks without a semaphore
    tasks = [asyncio.create_task(task(i)) for i in range(1000)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = [r for r in results if not isinstance(r, Exception)]
    failures = [r for r in results if isinstance(r, Exception)]
    for result in results:
        if isinstance(result, Exception):
            print(f"Error in task: {result}")
        else:
            print(f"Got result: {result}")

    print(f"✅ Completed: {len(successes)}")
    print(f"❌ Failed: {len(failures)}")
    print(f"⏱️  Total time: {time.time() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())