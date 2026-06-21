from executor.action_registry import (
    ACTION_REGISTRY
)


async def execute(
    page,
    step
):

    url = step.get("url") or step.get("target")

    await page.goto(url)

    return {
        "action": "goto",
        "status": "success"
    }


ACTION_REGISTRY["goto"] = execute