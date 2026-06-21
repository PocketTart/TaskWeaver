from executor.action_registry import (
    ACTION_REGISTRY
)


async def execute(
    page,
    step
):

    body_text = await page.locator(
        "body"
    ).inner_text()

    max_chars = step.get(
        "max_chars",
        12000
    )

    return {
        "action": "extract",
        "status": "success",
        "data": body_text[:max_chars]
    }


ACTION_REGISTRY["extract"] = execute