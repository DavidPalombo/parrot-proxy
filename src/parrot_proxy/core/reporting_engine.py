from datetime import datetime, timezone

def generate_markdown_report(campaign_name: str, workflow_results: list):
    timestamp = datetime.now(timezone.utc)

    lines = []

    lines.append(f"# Parrot Proxy Report")
    lines.append("")
    lines.append(f"Generated: {timestamp}")
    lines.append("")
    lines.append(f"Campaign: {campaign_name}")
    lines.append("")
    
    total_findings = 0

    for workflow in workflow_results:
        step = workflow["step"]

        results_data = workflow["results"]

        if isinstance(results_data, list):
            results = results_data
            clusters = {}
            outliers = {}
        else:
            results = results_data.get("results", [])
            clusters = results_data.get("clusters", {})
            outliers = results_data.get("outliers", {})

        lines.append(f"## Step: {step['type']}")
        lines.append("")
        lines.append(f"Total Results: {len(results)}")
        lines.append(
            f"Clusters: "
            f"{len(clusters)}"
        )
        lines.append(
            f"Outlier Clusters: "
            f"{len(outliers)}"
        )
        lines.append("")
        lines.append("| Payload | Status | Score |")
        lines.append("|---|---|---|")

        for item in results:
            result = item["result"]

            if result["error"]:
                continue

            mutation = item.get("mutation", {},)
            
            if isinstance(mutation, dict):
                payload = mutation.get("payload", "unknown",)

            else:
                payload = str(mutation)
        
            response = result["response"]

            score = item.get("score", {"score": 0})

            lines.append(
                f"| "
                f"{payload[:30]} | "
                f"{response.status_code} | "
                f"{score['score']} |"
            )

            if score["score"] >= 40:
                total_findings += 1
        
        lines.append("")

    lines.append("# Summary")
    lines.append("")
    lines.append(
        f"High Value Findings: "
        f"{total_findings}"
    )
    lines.append("")

    return "\n".join(lines)
