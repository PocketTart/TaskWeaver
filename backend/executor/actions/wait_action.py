from executor.action_registry import (
    ACTION_REGISTRY
)


async def execute(
    page,
    step
):

    await page.wait_for_timeout(
        step["duration"] * 1000
    )

    return {
        "action": "wait",
        "status": "success"
    }


ACTION_REGISTRY["wait"] = execute