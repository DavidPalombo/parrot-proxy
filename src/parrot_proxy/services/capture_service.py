from parrot_proxy.core.parser import parse_raw_request
from parrot_proxy.db.repository import save_request

def capture_request(raw_request: str):
    parsed = parse_raw_request(raw_request)

    saved_request = save_request(parsed)

    return saved_request