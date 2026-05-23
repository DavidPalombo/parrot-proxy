def score_response(
        status_code: int,
        baseline_status: int,
        body_lenght: int,
        baseline_length: int,
        reflection_detected: bool,
        response_time: float,
        baseline_time: float,
        redirect_location: str = None,
):
    # Score interesting responses.

    score = 0

    reasons = []

    if status_code != baseline_status:
        score += 25

        reasons.append("status changed")
    
    if reflection_detected:
        score += 40

        reasons.append("reflection detected")

    length_diff = abs(body_lenght - baseline_length)

    if length_diff > 500:
        score += 20

        reasons.append("large body difference")
    
    timing_diff = abs(response_time - baseline_time)

    if timing_diff > 2:
        score += 30

        reasons.append("timing anomaly")

    if redirect_location:
        score += 15

        reasons.append("redirect detected")

    if status_code >= 500:
        score += 35

        reasons.append("server error")

    return {
        "score": score,
        "reasons": reasons
    }