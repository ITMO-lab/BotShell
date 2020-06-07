# -*- coding: utf8 -*-

from main.core.application_async import AsyncApplication
from main.core.db.synchronized.local.discord.client import DiscordClient


class MainDiscord(AsyncApplication):
    @classmethod
    async def run(cls, message):
        channel = await DiscordClient.client.fetch_channel(message['message']['channel_id'])
        msg = await channel.fetch_message(message['message']['id'])
        user_id = message['message']['user_id']
        text = str(msg.content)
        message = None
        if text.startswith('dir'):
            message = await cls.dir()
        elif text.startswith('cd'):
            message = await cls.cd(user_id, text[2:].strip())
        elif text.startswith('pwd'):
            message = await cls.pwd()
        elif message is None:
            message = 'Неверная команда\nДоступные команды:\ndir\ncd\npwd'
        else:
            message = None
        await channel.send(str(message))

    @classmethod
    async def startup(cls, user_id):
        user = await DiscordClient.client.fetch_user(user_id)
        await user.create_dm()
        channel = user.dm_channel
        message = await cls.dir()
        await channel.send(str(message))
        message = await cls.dir()
        await channel.send(str(message))
