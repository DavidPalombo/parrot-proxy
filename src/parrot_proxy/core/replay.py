import httpx

def replay_request(
        method: str,
        url: str,
        headers: dict,
        body: str = None
):
    response = httpx.request(
        method = method,
        url = url,
        headers = headers,
        content = body,
        timeout = 15,
        follow_redirects = True,
    )

    return response