from typing import Dict

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