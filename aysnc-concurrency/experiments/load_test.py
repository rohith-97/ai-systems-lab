import asyncio
import aiohttp
import time

URL = "http://127.0.0.1:8000/infer"

async def fetch():
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=0, force_close=True)
    ) as session:
        async with session.get(URL) as response:
            return await response.json()

async def main():
    start = time.time()
    tasks = [fetch() for _ in range(5000)]
    await asyncio.gather(*tasks)
    print(f"Total time: {time.time() - start:.2f}s")

asyncio.run(main())