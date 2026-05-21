from parrot_proxy.core.diff_engine import compare_responses, detect_reflections
from parrot_proxy.services.replay_service import replay_saved_request

def compare_request_replays(
    request_id: int,
    modified_headers: list = None,
    modified_body: str = None,
):
    # Replay baseline and modified request, then compare.

    baseline = replay_saved_request(request_id)

    modified = replay_saved_request(
        request_id,
        override_headers = modified_headers,
        override_body = modified_body,
    )

    diff = compare_responses(
        baseline["response"],
        modified["response"],
    )

    reflection_detected = False
    
    if modified_body:
        reflection_detected = detect_reflections(
            modified["response"].text,
            modified_body,
        )

    return {
        "baseline": baseline["response"],
        "modified": modified["response"],
        "diff": diff,
        "reflection_detected": reflection_detected,
    }