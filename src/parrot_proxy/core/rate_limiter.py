import asyncio
import time

class RateLimiter:
    def __init__ (
            self,
            rate_per_second: int,
    ):
        self.rate = rate_per_second

        self.last_request = 0

    async def throttle(self):
        now = time.perf_counter()

        elapsed = (now - self.last_request)

        minimum_interval = (1 / self.rate)

        if elapsed < minimum_interval:
            await asyncio.sleep(
                minimum_interval - elapsed
            )

        self.last_request = (
            time.perf_counter()
        )