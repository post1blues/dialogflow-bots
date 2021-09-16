from telegram.ext import Updater, MessageHandler, Filters
from environs import Env
import telegram
import logging

from dialogflow_api import detect_intent_texts
from logging_handlers import TelegramLogsHandler

logger = logging.getLogger("tg_logger")


def send_answer(update, context):
    user_id = update.effective_user.id
    user_message = update.message.text
    answer = detect_intent_texts(user_id, user_message, language_code="ru")
    if answer:
        update.message.reply_text(answer)


def start_bot(bot_token):
    updater = Updater(bot_token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_answer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    env = Env()
    env.read_env(".env")

    tg_bot_token = env("TG_BOT_TOKEN")
    log_chat_id = env("LOG_CHAT_ID")

    tg_bot = telegram.Bot(token=tg_bot_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(log_chat_id, tg_bot))

    while True:
        start_bot(tg_bot_token)
