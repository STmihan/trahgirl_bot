import os
from dotenv import load_dotenv

load_dotenv()

YANDEX_SERVICE_ACC_ID = os.getenv("YANDEX_SERVICE_ACC_ID")
YANDEX_SERVICE_ACC_API_KEY = os.getenv("YANDEX_SERVICE_ACC_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
