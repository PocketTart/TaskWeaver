from executor.action_registry import (
    ACTION_REGISTRY
)
"""{
    "action": "click",
    "selector": "#submit"
}"""

async def execute(
    page,
    step
):

    await page.click(
        step["selector"]
    )

    return {
        "action": "click",
        "status": "success"
    }


ACTION_REGISTRY["click"] = execute