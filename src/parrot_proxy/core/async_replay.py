import asyncio
import httpx
import logging
import time

logger = logging.getLogger(__name__)

async def async_replay_request(
     method: str,
     url: str,
     headers: dict,
     body: str = None,   
):
    try:
        start = time.perf_counter()

        async with httpx.AsyncClient(
            timeout = 15,
            follow_redirects = True,
        ) as client:
            response = await client.request(
                method = method,
                url = url,
                headers = headers,
                content = body,
            )
        
        elapsed = time.perf_counter() - start

        return {
            "response": response,
            "elapsed": elapsed,
            "error": None,
        }
    except Exception as e:
        logger.exception("Async replay failed")

        return {
            "response": None,
            "elapsed": 0,
            "error": str(e),
        }