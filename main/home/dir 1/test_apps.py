# -*- coding: utf8 -*-

from main.core.application import Application
from main.core.event_handler.vk.tasks import mass_send


class TestApplication(Application):
    @classmethod
    def run(cls, message):
        user_id = int(message['object']['message']['from_id'])
        text = str(message['object']['message']['text'])
        message = 'Неверная команда\nДоступные команды:\ndir\ncd\npwd'
        if text.startswith('dir'):
            message = str(cls.dir())
        elif text.startswith('cd'):
            message = str(cls.cd(user_id, text[2:].strip()))
        elif text.startswith('pwd'):
            message = str(cls.pwd())
        messages = [message, ]
        user_ids = [[user_id, ], ]
        mass_send.apply_async(args=(messages, user_ids, ), queue='mass_send', priority=10)

    @classmethod
    def startup(cls, user_id):
        messages = (str(cls.dir()), )
        user_ids = ((user_id, ), )
        mass_send.apply_async(args=(messages, user_ids, ), queue='mass_send', priority=10)
