import asyncio
import json
import logging

from parrot_proxy.core.async_replay import async_replay_request
from parrot_proxy.core.diff_engine import is_interesting_response, detect_reflections
from parrot_proxy.core.param_mutator import mutate_query_parameter
from parrot_proxy.core.scoring_engine import score_response
from parrot_proxy.db.repository import get_request_by_id
from parrot_proxy.services.replay_service import replay_saved_request

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

    reflection_detected = False

    payload = mutation["payload"]

    score = {
        "score": 0,
        "reasons": [],
    }

    if result["response"]:
        reflection_detected = detect_reflections(
            result["response"].text,
            payload,
        )

        score = score_response(
            # TODO: Wire baseline analysis instead of using hardcoded values

            status_code = result["response"].status_code,
            baseline_status = 200,
            body_length = len(result["response"].text),
            baseline_length = 1000,
            reflection_detected = reflection_detected,
            response_time = result["elapsed"],
            baseline_time = 0.3,
            redirect_location = result["response"].headers.get("location"),
        )

    return {
        "mutation": mutation,
        "result": result,
        "score": score,
        "reflection_detected": reflection_detected,
    }

async def fuzz_parameters(
        request_id: int,
        payloads: list[str],
):
    saved = get_request_by_id(request_id)

    if not saved:
        raise Exception("Request not found")
    
    baseline = replay_saved_request(request_id)

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