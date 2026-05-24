import asyncio
import logging

from parrot_proxy.core.campaign_loader import load_campaign
from parrot_proxy.core.workflow_dispatcher import dispatch_step

logger = logging.getLogger(__name__)

async def run_campaign(campaign_path):
    campaign = load_campaign(campaign_path)

    logger.info(f"Running campaign ")
    f"{campaign_path}"

    workflow_results = []

    steps = campaign.get("steps", [])

    for step in steps:
        logger.info(
            f"Executing workflow step: " 
            f"{step['type']}"
        )

        results = await dispatch_step(step)

        workflow_results.append({
            "step": step,
            "results": results,
        })

    return workflow_results