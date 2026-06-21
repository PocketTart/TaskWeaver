from executor.action_registry import (
    ACTION_REGISTRY
)


async def execute(
    page,
    step
):

    query = step["query"]

    search_box = page.locator(
        "input[type='search'], input[type='text']"
    ).first

    await search_box.fill(
        query
    )

    await page.keyboard.press(
        "Enter"
    )

    return {
        "action": "search",
        "status": "success"
    }


ACTION_REGISTRY["search"] = execute