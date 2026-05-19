from parrot_proxy.core.parser import parse_raw_request

def capture_request(raw_request: str):
    parsed = parse_raw_request(raw_request)

    return parsed