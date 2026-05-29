import re

SQL_ERROR_PATTERNS = [
    r"sql syntax",
    r"mysql",
    r"postgresql",
    r"sqlite",
    r"odbc",
    r"database error",
    r"sqlstate",
]

XSS_PATTERNS = [
    r"<script",
    r"alert\(",
    r"onerror=",
    r"javascript:",
]

TRAVERSAL_PATTERNS = [
    r"root:x:",
    r"\[boot loader\]",
    r"/etc/passwd",
]

SSTI_PATTERNS = [
    r"49",
    r"jinja2",
    r"template error",
]

def detect_vulnerability_indicators(
        payload: str,
        response_text: str,
        status_code: int,
        reflection_analysis: dict,
):
    findings = []

    # SQLi logic
    for pattern in SQL_ERROR_PATTERNS:
        if re.search(pattern, response_text, re.IGNORECASE):
            findings.append({
                "type": "possible_sqli",
                "severity": "high",
                "reason": (
                    "SQL error pattern "
                    f"matched: {pattern}"
                ),
            })

    # XSS Logic
    if (reflection_analysis["severity"] == "high"):
        findings.append({
            "type": "possible_xss",
            "severity": "high",
            "reason": (
                "JavaScript reflection "
                "detected"
            ),
        }) 
    elif (reflection_analysis["severity"] == "medium"):
        findings.append({
            "type": "possible_xss",
            "severity": "medium",
            "reason": (
                "Attribute reflection "
                "detected"
            ),
        })

    # Traversal Logic
    for pattern in TRAVERSAL_PATTERNS:
        if re.search(pattern, response_text, re.IGNORECASE):
            findings.append({
                "type": "possible_traversal",
                "severity": "high",
                "reason": (
                    "Traversal indicator "
                    f"matched: {pattern}"
                ),
            })

    if "{{7*7}}" in payload:
        for pattern in SSTI_PATTERNS:
            if re.search(pattern, response_text, re.IGNORECASE):
                findings.append({
                    "type": "possible_ssti",
                    "severity": "high",
                    "reason": (
                        "Template evaluation "
                        "detected"
                    )
                })
    
    return findings
