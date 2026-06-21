import asyncio
from playwright.async_api import async_playwright


async def main():

    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=False
    )

    page = await browser.new_page()

    await page.goto(
        "https://google.com"
    )

    await page.wait_for_timeout(
        5000
    )

    await browser.close()

    await playwright.stop()


asyncio.run(main())