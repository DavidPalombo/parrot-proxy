from typing import Dict
from urllib.parse import urljoin

def parse_raw_request(raw_request: str) -> Dict:
    # Parse a raw HTTP request into structured data.

    lines = raw_request.strip().splitlines()

    request_line = lines[0]
    method, path, version = request_line.split()

    headers = {}
    body = ""

    is_body = False

    for line in lines[1:]:
        if line == "":
            is_body = True
            continue

        if not is_body:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
        else:
            body += line + "\n"
    
    return {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body.strip(),
    }

def parse_raw_http_request(raw_request: str,):
    lines = raw_request.splitlines()
    request_line = lines[0]

    method, path, _ = request_line.split()

    headers = {}

    body_start = None

    for i, line in enumerate(lines[1:], start = 1):
        if not line.strip():
            body_start = i + 1
            break

        key, value = line.splot(":", 1,)

        headers[key.strip()] = (value.strip())

    body = ""

    if body_start:
        body = "\n".join(lines[body_start:])

    host = headers.get("Host")

    if not host:
        raise ValueError("Host header required")
    
    url = f"https://{host}{path}"

    return{
        "method": method,
        "url": url,
        "headers": headers,
        "body": body,
    }