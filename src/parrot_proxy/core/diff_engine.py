def compare_responses(original, modified):
    # Compare two HTTP responses.

    differences = {
        "status_changed": original.status_code != modified.status_code,
        "original_status": original.status_code,
        "modified_status": modified.status_code,

        "body_length_changed": len(original.text) != len(modified.text),

        "original_length": len(original.text),
        "modified_length": len(modified.text),

        "new_headers": [],
    }

    original_headers = set(original.headers.keys())
    modified_headers = set(modified.headers.keys())

    differences["new_headers"] = list(
        modified_headers - original_headers
    )

    return differences

def detect_reflections(response_text: str, payload: str):
    # Detect if a payload is reflected in response

    return payload in response_text