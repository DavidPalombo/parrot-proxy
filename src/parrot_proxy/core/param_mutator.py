from urllib.parse import parse_qs, urlencode, urlparse

def mutate_query_parameter(
        path: str,
        payloads: list[str],
):
    # Generate mutated query parameter paths
    parsed = urlparse(path)

    query_params = parse_qs(parsed.query)

    mutations = []

    for param_name in query_params.keys():
        for payload in payloads:

            mutated_params = query_params.copy()

            mutated_params[param_name] = payload

            encoded = urlencode(
                mutated_params,
                doseq = True,
            )

            mutated_path = (
                f"{parsed.path}?{encoded}"
            )

            mutations.append({
                "parameter": param_name,
                "payload": payload,
                "path": mutated_path
            })

    return mutations