from parrot_proxy.core.parser import parse_raw_request, parse_raw_http_request
from parrot_proxy.db.repository import save_request

def capture_request(raw_request: str):
    parsed = parse_raw_request(raw_request)

    saved_request = save_request(parsed)

    return saved_request

def capture_request_file(path: str,):
    with open(path) as f:
        raw_request = f.read()

    parsed = (parse_raw_http_request(raw_request))

    return save_request(
        method = parsed["method"],
        url = parsed["url"],
        headers = parsed["headers"],
        body = parsed["body"],
    )