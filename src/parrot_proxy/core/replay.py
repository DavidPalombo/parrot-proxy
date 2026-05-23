import httpx
import logging
import time

logger = logging.getLogger(__name__)

def replay_request(
        method: str,
        url: str,
        headers: dict,
        body: str = None
):
    try:
        start = time.perf_counter()

        response = httpx.request(
            method = method,
            url = url,
            headers = headers,
            content = body,
            timeout = 15,
            follow_redirects = True,
        )

        elapsed = time.perf_counter() - start

        return {
            "response": response,
            "elapsed": elapsed,
            "error": None,
        }
    except httpx.ConnectTimeout:
        logger.exception("Connection timeout")

        return {
            "response": None,
            "elapsed": 0,
            "error": "Connection timeout",
        }
    
    except httpx.ConnectError:
        logger.exception("Connection error")

        return {
            "response": None,
            "elapsed": 0,
            "error": "Connection error",
        }
    
    except httpx.RequestError as e:
        logger.exception("Request failure")

        return {
            "response": None,
            "elapsed": 0,
            "error": str(e),
        }