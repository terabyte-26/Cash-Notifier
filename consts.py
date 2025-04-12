# Written by Hamza Farahat <farahat.hamza1@gmail.com>, 4/10/2025
# Contact me for more information:
# Contact Us: https://terabyte-26.com/quick-links/
# Telegram: @hamza_farahat or https://t.me/hamza_farahat
# WhatsApp: +212772177012


class HtmlElements(object):

    HISTORY_BTN: str = '//*[@id="main-content"]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/button'


class URLs(object):
    """
    URLs used in the project
    """

    STAKE_BASE_URL: str = "https://stake.com"
    CRASH_URL: str = f"{STAKE_BASE_URL}/casino/games/crash"
    STAKE_GRAPHQL_URL: str = f"{STAKE_BASE_URL}/_api/graphql"

    CHROME_DEV_TOOLS_URL: str = "http://localhost:9222"


class Consts(object):

    class Telegram(object):

        BOT_TOKEN: str = '7765386982:AAHK1WktL4DrwFVOfCkuOXMrGiJDs_VUox0'
        OWNER_ID: int = 1752221538
        MANOHAR_ID: int = 5958426402


class Temp(object):
    """
    Temporary variables used in the project
    """

    LAST_JSON_DATA: None | dict = None



