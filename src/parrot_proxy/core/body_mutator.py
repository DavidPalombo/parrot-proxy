from copy import deepcopy
import json

def mutate_json_body(body: str, payloads: list[str],):
    # Generate JSON body mutations

    try:
        parsed = json.loads(body)

    except Exception:
        return []
    
    mutations = []

    for key in parsed.keys():
        for payload in payloads:
            mutated = deepcopy(parsed)

            mutated[key] = payload

            mutations.append({
                "field": key,
                "payload": payload,
                "body": json.dumps(mutated),
            })

    return mutations
