# Written by Hamza Farahat <farahat.hamza1@gmail.com>, 4/10/2025
# Contact me for more information:
# Contact Us: https://terabyte-26.com/quick-links/
# Telegram: @hamza_farahat or https://t.me/hamza_farahat
# WhatsApp: +212772177012


import asyncio

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from consts import HtmlElements, URLs, Consts, Temp, Configs
from helpers import send_message, handle_response, countdown
from colorama import init, Fore, Style
from datetime import datetime


# Initialize colorama (important for Windows)
init(autoreset=True)


async def main():

    async with async_playwright() as p:
        # Connect to the existing Chrome instance

        try:
            # Connect to the existing Chrome instance
            browser: Browser = await p.chromium.connect_over_cdp(URLs.CHROME_DEV_TOOLS_URL)
        except Exception as e:
            print(f"[CONNECT]Error connecting to Chrome DevTools: {e}")
            raise e

        try:
            # Open a new page in an existing context
            context: BrowserContext = browser.contexts[0]  # Use existing context
            page: Page = await context.new_page()
        except Exception as e:
            print(f"[NEW_PAGE]Error opening new page: {e}")
            raise e


        try:

            try:
                # Navigate anywhere
                await page.goto(URLs.CRASH_URL)
            except Exception as e:
                print(f"[GOTO]Error navigating to URL: {e}")
                raise e

            # Wait for the page to
            try:
                await page.wait_for_selector(HtmlElements.HISTORY_BTN, timeout=30_000)
            except Exception as e:
                print(f"[WAIT_FOR_SELECTOR]Error waiting for selector: {e}")
                raise e

            try:
                # --- Listen to all network requests --
                page.on("response", lambda response: asyncio.create_task(handle_response(response)))
            except Exception as e:
                print(f"[LISTEN]Error listening to network requests: {e}")
                raise e

            print("Clicking the button...")
            try:
                await page.click(HtmlElements.HISTORY_BTN)
            except Exception as e:
                print(f"[CLICK]Error clicking the button: {e}")
                raise e

            print("Waiting for the crash game to load...")
            # Wait for the crash game to load
            while Temp.LAST_JSON_DATA is None:
                await asyncio.sleep(.2)

            # Check if Temp.LAST_JSON_DATA it contain a valid JSON
            if Temp.LAST_JSON_DATA is None:
                print("Temp.LAST_JSON_DATA is None")
                raise ValueError("Temp.LAST_JSON_DATA is None")

            # Get the crash game list from the JSON data
            cash_game_list: list[dict] = Temp.LAST_JSON_DATA.get("data", {}).get("crashGameList", [])

            # Check if the list is not empty
            if len(cash_game_list):

                middle_id: str = cash_game_list[0].get("id")
                print(f"Middle ID: {middle_id}")

                if Temp.PREVIOUS_MIDDLE_ID is not None and middle_id == Temp.PREVIOUS_MIDDLE_ID:
                    print(f"{Fore.LIGHTRED_EX} [MAIN] No new data received. Exiting...{Style.RESET_ALL}")
                    await page.close()
                    return

                else:
                    Temp.PREVIOUS_MIDDLE_ID = middle_id

                counter_values_above_threshold: int = 0
                message_text: str = ""

                for game in cash_game_list:

                    game_id: str = game.get("id")
                    start_time_str: str = game.get("startTime")
                    cash_point: str = game.get("crashpoint")

                    dt: datetime = datetime.strptime(start_time_str, '%a, %d %b %Y %H:%M:%S %Z')
                    start_time: str = dt.strftime('%H:%M:%S')

                    # Choose color based on crash point
                    if cash_point and float(cash_point) < Configs.POINT_THRESHOLD:
                        counter_values_above_threshold += 1
                        color = Fore.LIGHTRED_EX
                        message_text += f"<b><u>{start_time} --> <code>{cash_point:.3f}</code></u></b>\n"
                    else:
                        color = Fore.LIGHTYELLOW_EX
                        message_text += f"{start_time} --> <code>{cash_point:.3f}</code>\n"

                    print(f"{color}Start Time: {start_time}  -->  Cash Point: {cash_point:.3f}{Style.RESET_ALL}")

                print(f"\n{Fore.CYAN}Total games with cash point below {Configs.POINT_THRESHOLD}: {counter_values_above_threshold}{Style.RESET_ALL}")

                if counter_values_above_threshold >= Configs.HOW_MANY:

                    print("Sending message to Telegram...")

                    chats_list = [
                        Consts.Telegram.OWNER_ID,
                        # Consts.Telegram.MANOHAR_ID
                    ]

                    for chat_id in chats_list:
                        send_message(
                            chat_id=chat_id,
                            text=f"Crash game list with cash point below {Configs.POINT_THRESHOLD} within {Configs.HOW_MANY}:\n\n{message_text}",
                            silent=False
                        )

            else:
                print("No crash games list is empty.")
        except Exception as exception:
            print(f"{Fore.RED} [MAIN] An error occurred: {exception}{Style.RESET_ALL}")

        await page.close()


if __name__ == "__main__":
    # Run the main function
    print(f"{Fore.GREEN}Starting the script...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop the script.{Style.RESET_ALL}")

    while True:

        try:
            # Run the main function
            asyncio.run(main())
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Script stopped by user.{Style.RESET_ALL}")

        except:
            print(f"{Fore.RED}An error occurred: {Style.RESET_ALL}")
            print(f"{Fore.RED}Please check the logs for more details.{Style.RESET_ALL}")
        finally:
            print(f"{Fore.GREEN}Waiting for {Configs.SLEEP_TIME} seconds ({Configs.SLEEP_TIME // 60} minutes) before restarting...{Style.RESET_ALL}")
            countdown(Configs.SLEEP_TIME)

