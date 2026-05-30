from parrot_proxy.core.rule_engine import evaluate_rules

def test_regex_rule_matches():

    rules = [{
        "name": "SQL Leak",
        "match_regex": "sql syntax",
        "severity": "high",
        "score": 50,
    }]

    findings = evaluate_rules(
        response_text = "SQL syntax error",
        status_code = 500,
        headers = {},
        rules = rules,
    )

    assert len(findings) == 1

    assert findings[0]["name"] == "SQL Leak"

def test_status_rule_matches():

    rules = [{
        "name": "Server Error",
        "match_status": 500,
        "severity": "medium",
        "score": 20,
    }]

    findings = evaluate_rules(
        response_text = "",
        status_code = 500,
        headers = {},
        rules = rules,
    )

    assert len(findings) == 1