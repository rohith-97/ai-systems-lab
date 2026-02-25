import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(n: int):
    total =0
    for i in range (n):
        total += i
    return total

async def async_cpu(n: int):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(ProcessPoolExecutor(), cpu_heavy, n)
    return result

async def main():
    start = time.time()
    tasks = [async_cpu(10_000_000) for _ in range(10)]
    results = await asyncio.gather(*tasks)

    end = time.time()
    print(f"Total time: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())