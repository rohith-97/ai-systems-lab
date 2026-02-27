from fastapi import FastAPI
import asyncio
import random

app = FastAPI()

@app.get("/infer")
async def infer():
    await asyncio.sleep(5)  # increase latency
    return {"status": "ok"}