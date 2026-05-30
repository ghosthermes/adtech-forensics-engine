import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        har_path = os.path.join(os.getcwd(), "evidence.har")
        browser = await p.chromium.launch(headless=True)
        # Use a real User-Agent to prevent bot-blocking
        context = await browser.new_context(
            record_har_path=har_path,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print("Capturing high-fidelity traffic...")
        await page.goto("https://www.cnn.com", wait_until="load", timeout=60000)
        
        # Human-mimicry: Scroll to bottom to trigger lazy-loaded pixels
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        # Wait 15 seconds for all tracker pings to clear the queue
        await asyncio.sleep(15)
        
        await context.close()
        await browser.close()
        print(f"Capture complete. Evidence flushed to {har_path}")

if __name__ == "__main__":
    asyncio.run(run())
