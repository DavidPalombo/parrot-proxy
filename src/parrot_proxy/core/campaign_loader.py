import yaml

def load_campaign(path: str):
    with open(path) as f:
        return yaml.safe_load(f)