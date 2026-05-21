import json

from parrot_proxy.core.replay import replay_request
from parrot_proxy.db.repository import get_request_by_id

def replay_saved_request(
        request_id: int,
        override_method: str = None,
        override_body: str = None,
        override_headers: list = None,
):
    saved = get_request_by_id(request_id)

    if not saved:
        return None
    
    headers = json.loads(saved.headers)

    if override_headers:
        for header in override_headers:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()

    method = override_method or saved.method
    body = override_body or saved.body

    host = headers.get("Host")

    if not host:
        raise Exception("Missing Host Header")
    
    url = f"https://{host}{saved.path}"

    response = replay_request(
        method = method,
        url = url,
        headers = headers,
        body = body,
    )

    return {
        "request": saved,
        "response": response,
    }