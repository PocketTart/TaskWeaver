from executor.action_registry import (
    ACTION_REGISTRY
)


async def execute(
    page,
    step
):

    print(
        "SAVE RESULTS"
    )

    return {
        "action": "save_results",
        "status": "success"
    }


ACTION_REGISTRY["save_results"] = execute