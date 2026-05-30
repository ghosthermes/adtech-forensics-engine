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
        
        print(f"Executing resilient forensic capture on: {target_url}")
        try:
            # Drop the wait_until to 'domcontentloaded' to bypass ad bloat
            await page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
        except Exception:
            print("Page load taking too long, forcing execution sequence...")
            
        # Give JS frameworks 3 seconds to render the input fields
        await asyncio.sleep(3)
        
        # AUTOMATED PROBE
        try:
            email_inputs = await page.locator("input[type='email'], input[name*='email' i], input[id*='email' i]").all()
            if email_inputs:
                print(f"Found {len(email_inputs)} email fields. Injecting burner probe...")
                for input_field in email_inputs:
                    try:
                        await input_field.fill("xemnasvii@gmail.com")
                        await page.keyboard.press("Tab") # Trigger tracker listeners
                    except: pass
            else:
                print("No email fields found in the DOM.")
        except Exception as e:
            print(f"Probe injection failed: {e}")
            
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        print("Waiting 15 seconds for tracking pixels to exfiltrate data...")
        await asyncio.sleep(15) 
            
        await context.close()
        await browser.close()
        print(f"Log generated: {har_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python capture.py <url>")
    else:
        asyncio.run(run(sys.argv[1]))
