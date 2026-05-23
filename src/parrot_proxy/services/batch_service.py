import asyncio
import json
import logging

from parrot_proxy.core.async_replay import async_replay_request
from parrot_proxy.core.diff_engine import compare_responses
from parrot_proxy.db.repository import get_request_by_id

logger = logging.getLogger(__name__)

async def replay_mutation(saved, mutation):
    headers = json.loads(saved.headers)

    key, value = mutation.split(":", 1)

    headers[key.strip()] = value.strip()

    scheme = headers.get(
        "X-Parrot-Scheme",
        "https",
    )

    host = headers.get("Host")

    url = f"{scheme}://{host}{saved.path}"

    result = await async_replay_request(
        method = saved.method,
        url = url,
        headers = headers,
        body = saved.body,
    )

    return {
        "mutation": mutation,
        "result": result,
    }

async def run_batch_replay(
        request_id: int,
        mutations: list[str],
):
    saved = get_request_by_id(request_id)

    if not saved:
        raise Exception("Request not found")
    
    logger.info(
        f"Starting batch replay "
        f"for request #{request_id}"
    )

    tasks = []

    for mutation in mutations:
        tasks.append(
            replay_mutation(saved, mutation)
        )

    results = await asyncio.gather(*tasks)

    return results