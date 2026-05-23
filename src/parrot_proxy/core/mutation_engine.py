def generate_header_mutations (
        header_name: str,
        values: list[str],
):
    mutations = []

    for value in values:
        mutations.append(
            f"{header_name}: {value}"
        )
    
    return mutations