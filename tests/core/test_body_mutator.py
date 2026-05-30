from parrot_proxy.core.body_mutator import mutate_json_body

def test_json_body_mutation():

    body = """
    {
        "username": "admin",
        "password": "test"
    }
    """

    payloads = ["FUZZ"]

    mutations = mutate_json_body(body, payloads,)

    assert len(mutations) == 2

def test_invalid_json_returns_emtpy():

    mutations = mutate_json_body(
        "not-json",
        ["FUZZ"],
    )

    assert mutations == []