import asyncio
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

VIDEO_PATH = "/tmp/tiktok_upload.mp4"
COOKIES_PATH = sys.argv[1]  # e.g. /cookies/account_1.json
PROXY = sys.argv[2]         # e.g. http://user:pass@ip:port
CAPTION = "Posted with n8n 😎"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(proxy={"server": PROXY}, headless=False)
        context = await browser.new_context()

        # Load cookies
        if Path(COOKIES_PATH).exists():
            with open(COOKIES_PATH, "r") as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)
        else:
            print("❌ Cookie file not found.")
            await browser.close()
            sys.exit(1)

        page = await context.new_page()
        await page.goto("https://www.tiktok.com/upload", timeout=60000)

        # Upload video
        await page.set_input_files('input[type="file"]', VIDEO_PATH)
        await page.wait_for_timeout(5000)  # Wait for processing

        # Fill in caption
        await page.fill('textarea[data-e2e="upload-caption"]', CAPTION)

        # Click post button
        await page.click('button:has-text("Post")')

        # Wait and confirm
        await page.wait_for_timeout(10000)
        print("✅ Upload complete")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
