import re
import yaml

def load_rules(path = "rules/default.yaml"):
    with open(path) as f:
        data = yaml.safe_load(f)

    return data.get("rules", [])

def evaluate_rules(
        response_text: str,
        status_code: int,
        headers: dict,
        rules: list,
):
    findings = []

    for rule in rules:
        matched = False

        if "match_regex" in rule:
            pattern = rule["match_regex"]

            if re.search(pattern, response_text, re.IGNORECASE):
                matched = True

        if "match_status" in rule:
            if (status_code == rule["match_status"]):
                matched = True
        
        if "match_header" in rule:
            header_name = rule["match_header"]
            if header_name in headers:
                matched = True

        if matched:
            findings.append({
                "name": rule["name"],
                "severity": rule["severity"],
                "score": rule["score"],
            })

    return findings