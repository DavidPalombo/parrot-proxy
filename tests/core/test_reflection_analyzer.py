from parrot_proxy.core.reflection_analyzer import analyze_reflection_context

def test_detects_raw_reflections():

    result = analyze_reflection_context(
        payload = "admin",
        response_text = "<html>admin</html>",
    )

    assert result["reflected"] is True

    assert "raw" in result["contexts"]

def test_detects_attribute_reflection():

    result = analyze_reflection_context(
        payload = "admin",
        response_text = 'input value="admin">',
    )

    assert "attribute" in result["contexts"]
    
    assert result["severity"] == "medium"

def test_detects_javascript_reflection():

    result = analyze_reflection_context(
        payload = "admin",
        response_text = """
        <script>
        var user = "admin";
        </script>
        """,
    )

    assert "javascript" in result["contexts"]

    assert result["severity"] == "high"

