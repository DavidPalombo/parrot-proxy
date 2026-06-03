import asyncio
import json
import logging

from rich.console import Console

from parrot_proxy.core.async_replay import async_replay_request
from parrot_proxy.core.clustering_engine import cluster_responses, detect_outlier_cluster
from parrot_proxy.core.diff_engine import is_interesting_response, detect_reflections
from parrot_proxy.core.finding_engine import classify_severity
from parrot_proxy.core.fingerprint_engine import fingerprint_response
from parrot_proxy.core.heuristics_engine import detect_vulnerability_indicators
from parrot_proxy.core.param_mutator import mutate_query_parameter
from parrot_proxy.core.rate_limiter import RateLimiter
from parrot_proxy.core.reflection_analyzer import analyze_reflection_context
from parrot_proxy.core.rule_engine import load_rules, evaluate_rules
from parrot_proxy.core.scoring_engine import score_response
from parrot_proxy.core.worker_pool import WorkerPool
from parrot_proxy.db.repository import get_request_by_id, save_finding
from parrot_proxy.services.replay_service import replay_saved_request

logger = logging.getLogger(__name__)
console = Console()

async def replay_parameter_mutation(saved, mutation,):
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

    rules = load_rules()

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

    if score["score"] >= 40:
        severity = classify_severity(score["score"])

        save_finding(
            request_id = saved.id,
            severity = severity,
            score = score["score"],
            parameter = mutation["parameter"],
            payload = mutation["payload"],
            reason = ", ".join(score["reasons"]),
            status_code = result["response"].status_code,
            response_length = len(result["response"].text),
            reflection_detected = reflection_detected,
            response_time = str(result["elapsed"]),
        )

    response = result["response"]

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

        reflection_analysis = (
            analyze_reflection_context(
                payload = mutation["payload"],
                response_text = response.text,
            )
        )

        reflection_detected = (reflection_analysis["reflected"])

        heuristics = (
            detect_vulnerability_indicators(
                payload = mutation["payload"],
                response_text = response.text,
                status_code = response.status_code,
                reflection_analysis = reflection_analysis,
            )
        )

        rule_findings = (
            evaluate_rules (
                response_text = response.text,
                status_code = response.status_code,
                headers = dict(response.headers),
                rules = rules,
            )
        )

        console.print(reflection_analysis)
        console.print(heuristics)
        console.print(rule_findings)
        if (reflection_analysis["severity"] == "high"):
            score["score"] += 30
            score["reasons"].append("javascript reflection")
        elif (reflection_analysis["severity"] == "medium"):
            score["score"] += 15
            score["reasons"].append("attribute reflection")

        if heuristics:
            score["score"] += 40
            score["reasons"].append("vulnerability heuristics matched")

        for finding in rule_findings:
            score["score"] += (finding["score"])
            score["reasons"].append(
                f"rule matched: "
                f"{finding['name']}"
            )

        fingerprint = None

        if result["response"]:
            fingerprint = (
                fingerprint_response(
                    status_code = result["response"].status_code,
                    response_text = result["response"].text,
                    content_type = result["response"].headers.get(
                        "content-type",
                        "",
                    )
                )
            )

    return {
        "mutation": mutation,
        "result": result,
        "score": score,
        "reflection_detected": reflection_detected,
        "reflection_analysis": reflection_analysis,
        "fingerprint": fingerprint,
        "heuristics": heuristics,
        "rule_findings": rule_findings,
    }

async def fuzz_parameters(
        request_id: int,
        payloads: list[str],
        concurrency: int = 10,
        rate_limit: int = 5,
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

    pool = WorkerPool(concurrency = concurrency)
    limiter = RateLimiter(rate_per_second = rate_limit)

    tasks = []

    for mutation in mutations:
        await limiter.throttle()
        
        tasks.append(
            pool.run(
                replay_parameter_mutation(
                    saved,
                    mutation,
                )
            )
        )

    results = await asyncio.gather(*tasks)

    successful = [
        r for r in results
        if r["fingerprint"]
    ]

    clusters = cluster_responses(successful)

    outliers = detect_outlier_cluster(clusters)

    return {
        "results": results,
        "clusters": clusters,
        "outliers": outliers,
    }