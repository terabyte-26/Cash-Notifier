# Written by Hamza Farahat <farahat.hamza1@gmail.com>, 4/11/2025
# Contact me for more information:
# Contact Us: https://terabyte-26.com/quick-links/
# Telegram: @hamza_farahat or https://t.me/hamza_farahat
# WhatsApp: +212772177012
import json

import requests

from consts import Consts, Temp


async def handle_response(response):

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
                Temp.LAST_JSON_DATA = parsed
                # print(f"<<< Response: {response.status} {response.url}\nBody: {json.dumps(parsed, indent=4)}...\n")
    except Exception as e:
        print(f"Error reading response body from {response.url}: {e}")


def send_message(
        chat_id: int | str,
        text: str,
        silent: bool = False,
):
    """
    Sends a message to a chat using the Telegram Bot API. Optionally sends an image.

    Args:
        chat_id (int): The ID of the chat.
        text (str): The text of the message.
        message_thread_id (int, optional): The unique identifier of the message thread (topic). Defaults to None.
        image_url (str, optional): The URL of the image to send. Defaults to None.
        silent (bool, optional): Whether to send the message silently. Defaults to False.

    Returns:
        Response: The response from the Telegram Bot API.
    """
    try:

        # Define the standard data
        data: dict = {
            "chat_id": int(chat_id),
            "text": text,
            "parse_mode": "HTML",
            "disable_notification": silent,
        }

        method = "sendMessage"

        data['text'] = text

        url = f"https://api.telegram.org/bot{Consts.Telegram.BOT_TOKEN}/{method}"
        resp = requests.post(url, data=data, timeout=3, verify=False)

        if resp.json()["ok"] is False:
            print(resp.json())

        return resp
    except BaseException as e:
        print(f"An error occurred: {e}")
        pass

