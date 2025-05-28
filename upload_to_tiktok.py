import asyncio
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

VIDEO_PATH = "/tmp/tiktok_upload.mp4"
COOKIES_PATH = sys.argv[1]
PROXY = sys.argv[2]
CAPTION = "Posted with n8n 🤖"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(proxy={"server": PROXY}, headless=False)
        context = await browser.new_context()

        if Path(COOKIES_PATH).exists():
            with open(COOKIES_PATH, "r") as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto("https://www.tiktok.com/upload", timeout=60000)
        await page.set_input_files('input[type="file"]', VIDEO_PATH)
        await page.fill('textarea[data-e2e="upload-caption"]', CAPTION)
        await page.click('button:has-text("Post")')
        await page.wait_for_timeout(10000)

        print("✅ Upl
