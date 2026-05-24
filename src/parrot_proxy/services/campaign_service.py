import asyncio
import logging

from parrot_proxy.core.campaign_loader import load_campaign
from parrot_proxy.services.param_fuzz_service import fuzz_parameters

logger = logging.getLogger(__name__)

async def run_campaign(campaign_path: str,):
    campaign = load_campaign(campaign_path)

    logger.info(
        f"Running campaign: "
        f"{campaign_path}"
    )

    request_id = campaign["request_id"]

    mode = campaign["mode"]

    if mode == "fuzz-params":
        payloads = campaign["payloads"]

        results = await fuzz_parameters(
            request_id = request_id,
            payloads = payloads,
        )

        return {
            "mode": mode,
            "results": results,
        }
    
    raise Exception(
        f"Unsupported campaign mode: {mode}"
    )