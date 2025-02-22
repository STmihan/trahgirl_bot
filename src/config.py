import os
from dotenv import load_dotenv

load_dotenv()

TO_QUERY = [
    "анимешные",
    "сексуальные",
    "девушки",
    "арт",
    "эротические",
]

RATE_LIMIT_DAY = os.getenv("RATE_LIMIT_DAY")
RATE_LIMIT_GLOBAL = os.getenv("RATE_LIMIT_GLOBAL")


YANDEX_SERVICE_ACC_ID = os.getenv("YANDEX_SERVICE_ACC_ID")
YANDEX_SERVICE_ACC_API_KEY = os.getenv("YANDEX_SERVICE_ACC_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
