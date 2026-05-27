from parrot_proxy.core.mutation_engine import generate_header_mutations
from parrot_proxy.services.batch_service import run_batch_replay
from parrot_proxy.services.body_fuzz_service import fuzz_json_body
from parrot_proxy.services.param_fuzz_service import fuzz_parameters

async def dispatch_step(step: dict,):
    step_type = step["type"]

    request_id = step["request_id"]

    concurrency = step.get("concurrency", 10,)

    rate_limit = step.get("rate_limit", 5,)

    if step_type == "fuzz-params":
        payloads = step["payloads"]

        return await fuzz_parameters(
            request_id = request_id,
            payloads = payloads,
            concurrency = concurrency,
            rate_limit = rate_limit,
        )
    
    elif step_type == "fuzz-headers":
        header_name = step["header_name"]

        payloads = step["payloads"]

        mutations = (
            generate_header_mutations(
                header_name,
                payloads,
            )
        )

        return await run_batch_replay(
            request_id = request_id,
            mutations = mutations,
        )
    
    elif step_type == "fuzz-json":
        payloads = step["payloads"]

        return await fuzz_json_body(
            request_id = request_id,
            payloads = payloads,
        )

    raise Exception(
        f"Unsupported workflow step: "
        f"{step_type}"
    )