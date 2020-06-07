# -*- coding: utf8 -*-

from discord import ChannelType
from main.core.event_handler.discord.tasks import event_handler
from main.core.db.synchronized.redis.discord.admins_id_set import AdminsIdSet
from main.core.db.synchronized.redis.discord.users_id_set import UsersIdSet
from main.core.db.synchronized.redis.discord.directory_id_dictionary import DirectoryIdDictionary
from main.core.db.synchronized.local.base.event_type_enum import EventType
from main.core.db.synchronized.local.discord.client import DiscordClient
from main.core.event_handler.discord.tasks import users_id_set_sync, admins_id_set_sync, directory_id_set_sync

AdminsIdSet.sync()
UsersIdSet.sync()
DirectoryIdDictionary.sync()


async def obj_from_emoji(emoji_raw):
    emoji = {}
    try:
        emoji['str'] = str(emoji_raw)
    except:
        pass
    try:
        emoji['id'] = emoji_raw.id
        emoji['name'] = emoji_raw.name
        emoji['guild_id'] = emoji_raw.guild_id
    except:
        pass
    return emoji


@DiscordClient.client.event
async def on_ready():
    print('Logged on as', DiscordClient.client.user)
    print(DiscordClient.client.user.name)
    print(DiscordClient.client.user.id)
    print('------')


@DiscordClient.client.event
async def on_message(message):
    if message.author == DiscordClient.client.user or message.channel.type != ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_NEW,
           "message": {"id": message.id, "channel_id": message.channel.id, "user_id": message.author.id}}
    await event_handler(ctx)


@DiscordClient.client.event
async def on_message_delete(message):
    if message.author == DiscordClient.client.user or message.channel.type != ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_DELETE,
           "message": {"id": message.id, "channel_id": message.channel.id, "user_id": message.author.id}}
    await event_handler(ctx)


@DiscordClient.client.event
async def on_message_edit(before, after):
    if after.author == DiscordClient.client.user or after.channel.type != ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_EDIT,
           "message": {"id": after.id, "channel_id": after.channel.id, "user_id": after.author.id}}
    await event_handler(ctx)


@DiscordClient.client.event
async def on_reaction_add(reaction, user):
    if user == DiscordClient.client.user or reaction.message.channel.type != ChannelType.private:
        return
    ctx = {"type": EventType.REACTION_ADD,
           "reaction": {"count": reaction.count, "me": reaction.me, "user_id": user.id,
            "message": {"id": reaction.message.id, "channel_id": reaction.message.channel.id,
            "user_id": reaction.message.author.id}, "emoji": await obj_from_emoji(reaction.emoji)}}
    await event_handler(ctx)


@DiscordClient.client.event
async def on_reaction_remove(reaction, user):
    if user == DiscordClient.client.user or reaction.message.channel.type != ChannelType.private:
        return
    ctx = {"type": EventType.REACTION_REMOVE,
           "reaction": {"count": reaction.count, "me": reaction.me, "user_id": user.id,
            "message": {"id": reaction.message.id, "channel_id": reaction.message.channel.id,
            "user_id": reaction.message.author.id}, "emoji": await obj_from_emoji(reaction.emoji)}}
    await event_handler(ctx)

users_id_set_sync()
admins_id_set_sync()
directory_id_set_sync()

DiscordClient.client.run(DiscordClient.token)
