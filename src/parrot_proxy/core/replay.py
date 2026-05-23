import httpx
import time

def replay_request(
        method: str,
        url: str,
        headers: dict,
        body: str = None
):
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
        "elapsed": elapsed
    }