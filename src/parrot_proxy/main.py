from parrot_proxy.cli.commands import app
from parrot_proxy.config.logging_config import setup_logging

setup_logging()

if __name__ == "__main__":
    app()