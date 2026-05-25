from parrot_proxy.core.mutation_engine import generate_header_mutations
from parrot_proxy.services.batch_service import run_batch_replay
from parrot_proxy.services.param_fuzz_service import fuzz_parameters

async def dispatch_step(step: dict,):
    step_type = step["type"]

    request_id = step["request_id"]

    if step_type == "fuzz-params":
        payloads = step["payloads"]

        return await fuzz_parameters(
            request_id = request_id,
            payloads = payloads,
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

    raise Exception(
        f"Unsupported workflow step: "
        f"{step_type}"
    )