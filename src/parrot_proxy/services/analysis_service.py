import logging

from parrot_proxy.core.diff_engine import compare_responses, detect_reflections
from parrot_proxy.db.repository import save_replay_history
from parrot_proxy.services.replay_service import replay_saved_request

logger = logging.getLogger(__name__)

def compare_request_replays(
    request_id: int,
    modified_headers: list = None,
    modified_body: str = None,
):
    # Replay baseline and modified request, then compare.

    logger.info(
        f"Running comparison analysis"
        f"for request #{request_id}"
    )

    baseline = replay_saved_request(request_id)

    modified = replay_saved_request(
        request_id,
        override_headers = modified_headers,
        override_body = modified_body,
    )

    diff = compare_responses(
        baseline["response"],
        modified["response"],
        baseline["elapsed"],
        modified["elapsed"],

    )

    reflection_detected = False
    
    if modified_body:
        reflection_detected = detect_reflections(
            modified["response"].text,
            modified_body,
        )
    
    if reflection_detected:
        logger.warning("Reflection detected in response")

    save_replay_history(
        request_id = request_id,
        replay_method = modified["request"].method,
        replay_url = str(modified["response"].url),
        status_code = modified["response"].status_code,
        response_length = len(modified["response"].text),
        reflection_detected = reflection_detected,
        diff_status_changed = diff["status_changed"],
        diff_body_changed = diff["body_length_changed"],
    )
    return {
        "baseline": baseline["response"],
        "modified": modified["response"],
        "diff": diff,
        "reflection_detected": reflection_detected,
    }