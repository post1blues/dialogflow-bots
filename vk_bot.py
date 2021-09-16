import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from environs import Env
import telegram
import logging

from dialogflow_api import detect_intent_texts
from logging_handlers import TelegramLogsHandler


logger = logging.getLogger("vk_logger")


def send_answer(event, vk_api):
    message = event.text
    session_id = event.user_id
    response_message = detect_intent_texts(session_id, message)

    if response_message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_message,
            random_id=get_random_id()
        )


def start_bot(bot_token):
    vk_session = vk.VkApi(token=bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_answer(event, vk_api)


if __name__ == "__main__":
    env = Env()
    env.read_env(".env")
    VK_BOT_TOKEN = env("VK_BOT_TOKEN")

    TG_BOT_TOKEN = env("TG_BOT_TOKEN")
    LOG_CHAT_ID = env("LOG_CHAT_ID")

    tg_bot = telegram.Bot(token=TG_BOT_TOKEN)

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(LOG_CHAT_ID, tg_bot))

    start_bot(VK_BOT_TOKEN)