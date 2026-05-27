import asyncio
import json
import logging

from parrot_proxy.core.async_replay import async_replay_request
from parrot_proxy.core.body_mutator import mutate_json_body
from parrot_proxy.core.finding_engine import classify_severity
from parrot_proxy.core.scoring_engine import score_response
from parrot_proxy.db.repository import get_request_by_id, save_finding

logger = logging.getLogger(__name__)

async def replay_body_mutation(saved, mutation,):
    headers = json.loads(saved.headers)

    scheme = headers.get(
        "X-Parrot-Scheme",
        "https",
    )

    host = headers.get("Host")

    url = (
        f"{scheme}://"
        f"{host}"
        f"{saved.path}"
    )

    result = await async_replay_request(
        method = saved.method,
        url = url,
        headers = headers,
        body = mutation["body"],
    )

    score = {
        "score": 0,
        "reasons": [],
    }

    if result["response"]:
        response = result["response"]

        score = score_response(
            status_code = response.status_code,
            baseline_status = 200,
            body_length = len(response.text),
            baseline_length = 1000,
            reflection_detected = False,
            response_time = result["elapsed"],
            baseline_time = 0.3,
            redirect_location = response.headers.get("location"),
        )

        if score["score"] >= 40:
            severity = classify_severity(score["score"])

            save_finding(
                request_id = saved.id,
                severity = severity,
                score = score["score"],
                parameter = mutation["field"],
                payload = mutation["payload"],
                reason = ", ".join(score["reasons"]),
                status_code = response.status_code,
                response_length = len(response.text),
                reflection_detected = False,
                response_time = str(result["elapsed"]),
            )
    return {
        "mutation": mutation,
        "result": result,
        "score": score,
    }

async def fuzz_json_body(request_id: int, payloads: list[str]):
    saved = get_request_by_id(request_id)

    if not saved:
        raise Exception("Request not found")
    
    mutations = mutate_json_body(saved.body, payloads,)

    logger.info(
        f"Generated "
        f"{len(mutations)} body mutations"
    )

    tasks = []

    for mutation in mutations:
        tasks.append(replay_body_mutation(saved, mutation,))

    results = await asyncio.gather(*tasks)

    return results