import asyncio
from playwright.async_api import async_playwright

async def _capture(html_string, output_path, width=800, height=600):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": width, "height": height})
        await page.set_content(html_string)
        await page.screenshot(path=output_path)
        await browser.close()

def capture_screenshot(html_string, output_path, width=800, height=600):
    asyncio.run(_capture(html_string, output_path, width, height))