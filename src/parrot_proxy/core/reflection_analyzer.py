import html
import re
import urllib.parse

def anaylze_reflection(payload: str, response_text: str,):
    findings = []

    # Raw reflection
    if payload in response_text:
        findings.append({
            "type": "raw",
            "severity": "medium",
        })

    #HTML encoded reflection
    encoded = html.escape(payload)

    if encoded in response_text:
        findings.append({
            "type": "html_encoded",
            "severity": "low",
        })

    # URL encoded reflection
    url_encoded = urllib.parse.quote(payload)

    if url_encoded in response_text:
        findings.append({
            "type": "url_encoded",
            "severity": "low",
        })

    return findings

def detect_javascript_context(payload: str, response_text: str,):
    patterns = [rf"script.*?>.*?{re.escape(payload)}.*?</script>",]

    for pattern in patterns:
        if re.search(pattern, response_text, re.IGNORECASE | re.DOTALL, ):
            return True
        
    return False

def detect_attribute_context(payload: str, response_text: str,):
    patterns = [
        rf'="[^"]*{re.escape(payload)}[^"]*"',
        rf"='[^']*{re.escape(payload)}[^']*'",
    ]

    for pattern in patterns:
        if re.search(pattern, response_text, re.IGNORECASE):
            return True
    
    return False

def analyze_reflection_context(payload: str, response_text: str,):
    results = {
        "reflected": False,
        "contexts": [],
        "severity": "none",
    }

    reflections = anaylze_reflection(payload, response_text)

    if reflections:
        results["reflected"] = True

    for reflection in reflections:
        results["contexts"].append(reflection["type"])

    if detect_javascript_context(payload, response_text,):
        results["contexts"].append("javascript")
        results["severity"] = "high"

    if detect_attribute_context(payload, response_text,):
        results["contexts"].append("attribute")

        if results["severity"] != "high":
            results["severity"] = "medium"

    if (reflections and results["severity"] == "none"):
        results["seveirty"] = "low"

    return results

    