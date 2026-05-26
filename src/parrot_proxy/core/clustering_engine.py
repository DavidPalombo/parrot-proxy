def cluster_responses(response_items: list,):
    # Group similar response together

    for item in response_items:
        fingerprint = item["fingerprint"]

        clusters = {}

        for item in response_items:
            fingerprint = item["fingerprint"]

            cluster_key = (
                f"{fingerprint['status_code']}_"
                f"{fingerprint['body_length']}_"
                f"{fingerprint['hash']}"
            )

            if cluster_key not in clusters:
                clusters[cluster_key] = []

            clusters[cluster_key].append(item)

        return clusters
    
def detect_outlier_cluster(
        clusters: dict,
        threshold: int = 2,
):
    outliers = {}

    for key, items in clusters.items():
        if len(items) <= threshold:
            outliers[key] = items
    
    return outliers