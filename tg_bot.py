from telegram.ext import Updater, MessageHandler, Filters
from environs import Env
import logging
import textwrap

from dialogflow_api import detect_intent_texts
from logging_handlers import TelegramLogsHandler

logger = logging.getLogger("tg_logger")


def send_answer(update, context):
    user_id = update.effective_user.id
    user_message = update.message.text
    response_message = detect_intent_texts(user_id, user_message, language_code="ru")
    if response_message:
        update.message.reply_text(response_message)
    else:
        response_message = f"""\
                Пользователь {user_id} оставил сообщение в vk.com.
                Бот не знает, что ответить, поэтому требуется присутствие менеджера!
                """
        logger.warning(textwrap.dedent(response_message))


def start_bot(bot_token):
    logger.warning("Telegram bot starts working")

    updater = Updater(bot_token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_answer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    env = Env()
    env.read_env(".env")

    TG_BOT_TOKEN = env("TG_BOT_TOKEN")
    LOG_CHAT_ID = env("LOG_CHAT_ID")

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(LOG_CHAT_ID, TG_BOT_TOKEN))

    start_bot(TG_BOT_TOKEN)
