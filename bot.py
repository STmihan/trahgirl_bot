import random

from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler

from src.config import BOT_TOKEN, TO_QUERY
from src.rate_limits import check_and_update_rate_limit
from src.services.image_service import get_random_image_url, download_image


def request_image(retries=5):
    try:
        random.shuffle(TO_QUERY)
        query = " ".join(TO_QUERY)
        img = get_random_image_url(query)
        path = download_image(img, "data")
        return path
    except Exception as e:
        print(e)
        retries -= 1
        print("Failed to fetch image. Retrying...")
        return request_image(retries) if retries > 0 else None


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    error_message = check_and_update_rate_limit(user_id)
    if error_message:
        await context.bot.send_message(update.message.chat_id, error_message)
        return

    path = request_image()
    if path is not None:
        await context.bot.send_photo(update.message.chat_id, photo=open(path, "rb"))
    else:
        await context.bot.send_message(update.message.chat_id, "Ошибка при загрузке изображения.")


def start_bot():
    print("Starting bot")
    app = (ApplicationBuilder()
           .token(BOT_TOKEN)
           .build())
    app.add_handler(MessageHandler(filters=None, callback=on_message))
    app.run_polling()


if __name__ == '__main__':
    start_bot()
