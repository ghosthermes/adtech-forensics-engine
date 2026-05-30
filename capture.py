import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def run(target_url):
    async with async_playwright() as p:
        har_path = os.path.join(os.getcwd(), "evidence.har")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_har_path=har_path,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"Executing forensic capture on: {target_url}")
        try:
            await page.goto(target_url, wait_until="load", timeout=60000)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(15) # Wait for pixel fire
        except Exception as e:
            print(f"Error during capture: {e}")
            
        await context.close()
        await browser.close()
        print(f"Log generated: {har_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python capture.py <url>")
    else:
        asyncio.run(run(sys.argv[1]))
