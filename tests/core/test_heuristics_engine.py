from parrot_proxy.core.heuristics_engine import detect_vulnerability_indicators

def test_detects_sqli():

    findings = (
        detect_vulnerability_indicators(
            payload = "' OR 1=1 --",
            response_text = """You have an error in your SQL syntax""",
            status_code = 500,
            reflection_analysis = {"severity": "none",}
        )
    )

    assert any(
        f["type"] == "possible_sqli"
        for f in findings
    )

def test_detects_path_traversal():

    findings = (
        detect_vulnerability_indicators(
            payload = "../../../etc/passwd",
            response_text = """root:x:0:0:root""",
            status_code = 200,
            reflection_analysis = {"severity": "none",},
        )
    )

    assert any(
        f["type"] == "possible_traversal"
        for f in findings
    )

def test_detects_xss():
    
    findings = (
        detect_vulnerability_indicators(
            payload = "<script>alert(1)</script>",
            response_text = "ignored",
            status_code = 200,
            reflection_analysis = {"severity": "high",},
        )
    )

    assert any(
        f["type"] == "possible_xss"
        for f in findings
    )