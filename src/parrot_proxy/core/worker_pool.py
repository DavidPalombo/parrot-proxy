import asyncio

class WorkerPool:
    def __init__(self, concurrency: int = 10,):
        self.semaphore = asyncio.Semaphore(concurrency)

    async def run(self, coro,):
        async with self.semaphore:
            return await coro