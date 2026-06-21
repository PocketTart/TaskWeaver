from playwright.async_api import (
    async_playwright
)


class PlaywrightClient:

    async def get_page(self):

        playwright = await (
            async_playwright().start()
        )

        browser = await (
            playwright.chromium.launch(
                headless=True
            )
        )

        page = await browser.new_page()

        return (
            playwright,
            browser,
            page
        )