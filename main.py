# Written by Hamza Farahat <farahat.hamza1@gmail.com>, 4/10/2025
# Contact me for more information:
# Contact Us: https://terabyte-26.com/quick-links/
# Telegram: @hamza_farahat or https://t.me/hamza_farahat
# WhatsApp: +212772177012


import asyncio
import json

from playwright.async_api import async_playwright


LAST_JSON_DATA: None | dict = None


async def main():

    global LAST_JSON_DATA

    async with async_playwright() as p:
        # Connect to the existing Chrome instance
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")

        # Open a new page in an existing context (or use browser.contexts[0])
        context = browser.contexts[0]  # Use existing context
        page = await context.new_page()

        # Navigate anywhere
        await page.goto("https://stake.com/casino/games/crash")

        # --- Listen to all network requests ---
        await page.wait_for_selector('//*[@id="main-content"]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/button', timeout=20_000)

        # page.on("request", lambda request: print(f">>> Request: {request.method} {request.url}"))
        page.on("response", lambda response: asyncio.create_task(handle_response(response)))

        print("Clicking the button...")
        await page.click('//*[@id="main-content"]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/button')

        print("Waiting for the crash game to load...")

        while LAST_JSON_DATA is None:
            await asyncio.sleep(.2)

        print(json.dumps(LAST_JSON_DATA, indent=4))

        await page.close()


async def handle_response(response):
    global LAST_JSON_DATA
    try:
        # Only get text/html or JSON to avoid binary mess
        content_type = response.headers.get("content-type", "")
        if ("application/json" in content_type or "text" in content_type) and (response.url == 'https://stake.com/_api/graphql'):

            body_string: str = await response.text()

            try:
                parsed = json.loads(body_string)

            except:
                parsed = None

            if parsed and isinstance(parsed, dict) and parsed.get("data", {}).get("crashGameList", None) is not None:
                LAST_JSON_DATA = parsed
                # print(f"<<< Response: {response.status} {response.url}\nBody: {json.dumps(parsed, indent=4)}...\n")
    except Exception as e:
        print(f"Error reading response body from {response.url}: {e}")

asyncio.run(main())
