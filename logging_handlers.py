import logging


class TelegramLogsHandler(logging.Handler):
    def __init__(self, log_chat_id, tg_bot):
        super().__init__()
        self.log_chat_id = log_chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.log_chat_id, text=log_entry)