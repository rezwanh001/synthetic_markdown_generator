# src/image_capturer.py

import asyncio
from playwright.async_api import async_playwright

async def _render_and_capture(html_string, png_path=None, pdf_path=None, width=800):
    """
    An internal async function to launch a browser and capture a PNG and/or a PDF.
    This is more efficient as it only launches the browser once.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Set a default viewport width. The height doesn't matter for full-page screenshots.
        await page.set_viewport_size({"width": width, "height": 800})
        
        # Load the HTML content
        await page.set_content(html_string, wait_until="networkidle")

        # --- Capture PNG Screenshot if path is provided ---
        if png_path:
            await page.screenshot(
                path=png_path,
                full_page=True  # THIS IS THE FIX for incomplete images
            )

        # --- Capture PDF if path is provided ---
        if pdf_path:
            await page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True, # Important for capturing custom CSS backgrounds
                margin={'top': '20mm', 'bottom': '20mm', 'left': '20mm', 'right': '20mm'}
            )
            
        await browser.close()

def render_and_capture(html_string, png_path=None, pdf_path=None, width=800):
    """
    Synchronous wrapper to render HTML and capture a screenshot and/or a PDF.

    Args:
        html_string (str): The HTML content to render.
        png_path (str, optional): The file path to save the PNG image. Defaults to None.
        pdf_path (str, optional): The file path to save the PDF document. Defaults to None.
        width (int, optional): The viewport width for rendering. Defaults to 800.
    """
    if not png_path and not pdf_path:
        print("Warning: render_and_capture called without any output paths (png_path or pdf_path).")
        return
        
    asyncio.run(_render_and_capture(html_string, png_path, pdf_path, width))