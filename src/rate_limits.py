import time
import datetime

from src.config import RATE_LIMIT_GLOBAL, RATE_LIMIT_DAY

user_limits = {}

global_limit = {
    "daily_count": 0,
    "day": datetime.date.today()
}

ERROR_MESSAGE = "Слишком часто! Пожалуйста, подождите немного."


def check_and_update_rate_limit(user_id: int) -> str | None:
    now = time.time()
    today = datetime.date.today()

    if global_limit["day"] != today:
        global_limit["daily_count"] = 0
        global_limit["day"] = today

    if global_limit["daily_count"] >= RATE_LIMIT_GLOBAL:
        return ERROR_MESSAGE

    if user_id not in user_limits:
        user_limits[user_id] = {"last_request": 0, "daily_count": 0, "day": today}
    elif user_limits[user_id]["day"] != today:
        user_limits[user_id]["daily_count"] = 0
        user_limits[user_id]["day"] = today

    if now - user_limits[user_id]["last_request"] < 1:
        return ERROR_MESSAGE

    if user_limits[user_id]["daily_count"] >= RATE_LIMIT_DAY:
        return ERROR_MESSAGE

    global_limit["daily_count"] += 1
    user_limits[user_id]["last_request"] = now
    user_limits[user_id]["daily_count"] += 1

    return None
