from executor.action_registry import (
    ACTION_REGISTRY
)
"""{
    "action": "fill",
    "selector": "#email",
    "value": "abc@test.com"
}"""

async def execute(
    page,
    step
):

    await page.fill(
        step["selector"],
        step["value"]
    )

    return {
        "action": "fill",
        "status": "success"
    }


ACTION_REGISTRY["fill"] = execute