# Written by Hamza Farahat <farahat.hamza1@gmail.com>, 4/10/2025
# Contact me for more information:
# Contact Us: https://terabyte-26.com/quick-links/
# Telegram: @hamza_farahat or https://t.me/hamza_farahat
# WhatsApp: +212772177012


import asyncio
import json
from datetime import datetime

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from consts import HtmlElements, URLs
from colorama import init, Fore, Style

# Initialize colorama (important for Windows)
init(autoreset=True)

LAST_JSON_DATA: None | dict = None
POINT_THRESHOLD: float | int = 2
HOW_MANY: int = 7


async def main():

    global LAST_JSON_DATA

    async with async_playwright() as p:
        # Connect to the existing Chrome instance
        browser: Browser = await p.chromium.connect_over_cdp(URLs.CHROME_DEV_TOOLS_URL)

        # Open a new page in an existing context
        context: BrowserContext = browser.contexts[0]  # Use existing context
        page: Page = await context.new_page()

        # Navigate anywhere
        await page.goto(URLs.CRASH_URL)

        # Wait for the page to load
        await page.wait_for_selector(HtmlElements.HISTORY_BTN, timeout=20_000)

        # --- Listen to all network requests --
        page.on("response", lambda response: asyncio.create_task(handle_response(response)))

        print("Clicking the button...")
        await page.click(HtmlElements.HISTORY_BTN)

        print("Waiting for the crash game to load...")
        # Wait for the crash game to load
        while LAST_JSON_DATA is None:
            await asyncio.sleep(.2)

        # Get the crash game list from the JSON data
        cash_game_list: list[dict] = LAST_JSON_DATA.get("data", {}).get("crashGameList", [])

        # Check if the list is not empty
        if len(cash_game_list):

            counter_values_above_threshold: int = 0

            for game in cash_game_list:

                game_id: str = game.get("id")
                start_time_str: str = game.get("startTime")
                cash_point: str = game.get("crashpoint")

                dt: datetime = datetime.strptime(start_time_str, '%a, %d %b %Y %H:%M:%S %Z')
                start_time: str = dt.strftime('%H:%M:%S')

                # Choose color based on crash point
                if cash_point and float(cash_point) < POINT_THRESHOLD:
                    counter_values_above_threshold += 1
                    color = Fore.LIGHTRED_EX
                else:
                    color = Fore.LIGHTYELLOW_EX

                print(f"{color}Start Time: {start_time}  -->  Cash Point: {cash_point:.3f}{Style.RESET_ALL}")

            print(f"\n{Fore.CYAN}Total games with cash point below {POINT_THRESHOLD}: {counter_values_above_threshold}{Style.RESET_ALL}")
        else:
            print("No crash games list is empty.")

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
