def build_url(
        scheme: str,
        host: str,
        path: str,
):
    return f"{scheme}://{host}{path}"