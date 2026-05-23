import asyncio
import json
import logging

from parrot_proxy.core.async_replay import async_replay_request
from parrot_proxy.core.diff_engine import is_interesting_response
from parrot_proxy.core.param_mutator import mutate_query_parameter
from parrot_proxy.db.repository import get_request_by_id

logger = logging.getLogger(__name__)

async def replay_parameter_mutation(
        saved,
        mutation
):
    headers = json.loads(saved.headers)

    scheme = headers.get(
        "X-Parrot-Scheme",
        "https",
    )

    host = headers.get("Host")

    url = (
        f"{scheme}://"
        f"{host}"
        f"{mutation['path']}"
    )

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

async def fuzz_parameters(
        request_id: int,
        payloads: list[str],
):
    saved = get_request_by_id(request_id)

    if not saved:
        raise Exception("Request not found")
    
    mutations = mutate_query_parameter(
        saved.path,
        payloads,
    )

    logger.info(
        f"Generated "
        f"{len(mutations)} parameter mutations"
    )

    tasks = []

    for mutation in mutations:
        tasks.append(
            replay_parameter_mutation(
                saved,
                mutation
            )
        )

    results = await asyncio.gather(*tasks)

    return results