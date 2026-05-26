import hashlib

def fingerprint_response(
        status_code: int,
        response_text: str,
        content_type: str = "",
):
    # Lightweight response fingerprint

    normalized = (
        response_text[:1000].strip().lower()
    )

    response_hash = hashlib.md5(normalized.encode()).hexdigest()

    return {
        "status_code": status_code,
        "content_type": content_type,
        "body_length": len(response_text),
        "hash": response_hash,
    }