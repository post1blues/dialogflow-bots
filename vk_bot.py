import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from environs import Env
import logging
import textwrap

from dialogflow_api import detect_intent_texts
from logging_handlers import TelegramLogsHandler


logger = logging.getLogger("vk_logger")


def send_answer(event, vk_api):
    message = event.text
    user_id = event.user_id
    response_message = detect_intent_texts(user_id, message)

    if response_message:
        vk_api.messages.send(
            user_id=user_id,
            message=response_message,
            random_id=get_random_id()
        )
    else:
        response_message = f"""\
        Пользователь {user_id} оставил сообщение в vk.com.
        Бот не знает, что ответить, поэтому требуется присутствие менеджера!
        """
        logger.warning(textwrap.dedent(response_message))


def start_bot(bot_token):
    logger.warning("VK bot starts working")

    vk_session = vk.VkApi(token=bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_answer(event, vk_api)


def main():
    env = Env()
    env.read_env(".env")
    vk_bot_token = env("VK_BOT_TOKEN")

    tg_bot_token = env("TG_BOT_TOKEN")
    log_chat_id = env("LOG_CHAT_ID")

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(log_chat_id, tg_bot_token))

    start_bot(vk_bot_token)


if __name__ == "__main__":
    main()