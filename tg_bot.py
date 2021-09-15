from telegram.ext import Updater, MessageHandler, Filters
from environs import Env

from dialogflow_api import detect_intent_texts


def send_answer(update, context):
    user_id = update.effective_user.id
    user_message = update.message.text
    answer = detect_intent_texts(user_id, user_message, language_code="ru")
    if answer:
        update.message.reply_text(answer)


def start_bot():
    updater = Updater(TG_BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_answer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    env = Env()
    env.read_env(".env")
    TG_BOT_TOKEN = env("TG_BOT_TOKEN")

    start_bot()
