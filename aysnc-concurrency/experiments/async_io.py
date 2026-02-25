import asyncio
import time
from tqdm.asyncio import tqdm

async def task(task_id: int, semaphore: asyncio.Semaphore):
    async with semaphore:
        await asyncio.sleep(0.1)
        if task_id == 500:
            raise ValueError(f"Task {task_id} encountered an error")
        return f"Task {task_id} completed"

async def main():
    start = time.time()
    semaphore = asyncio.Semaphore(100)  # Limit concurrency to 100  
    tasks = [asyncio.create_task(task(i, semaphore)) for i in range(1000)]
    results = []
    for future in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        try:
            result = await future
            results.append(result)
            print(f"Got result: {result}")
        except Exception as e:
            results.append(e)
            print(f"Error in task: {e}")

    successes = [r for r in results if not isinstance(r, Exception)]
    failures = [r for r in results if isinstance(r, Exception)]
    
    print(f"✅ Completed: {len(successes)}")
    print(f"❌ Failed: {len(failures)}")
    print(f"⏱️  Total time: {time.time() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())