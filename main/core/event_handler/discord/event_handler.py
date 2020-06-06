# -*- coding: utf8 -*-

import discord
from main.core.event_handler.discord.tasks import event_handler
from main.core.db.synchronized.redis.discord.admins_id_set import AdminsIdSet
from main.core.db.synchronized.redis.discord.users_id_set import UsersIdSet
from main.core.db.synchronized.redis.discord.directory_id_dictionary import DirectoryIdDictionary
from main.core.event_handler.discord.event_type_enum import EventType
import os

cur_dir = '/main/core/event_handler/discord'
path = os.getcwd()
if path.count(cur_dir) == 0:
    path += '/main/core/event_handler/discord'
with open(path + '/token.secret') as file:
    confirmation_token = file.readline()

AdminsIdSet.sync()
UsersIdSet.sync()
DirectoryIdDictionary.sync()

permissions = discord.Permissions()
permissions.all()
client = discord.Client()


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


@client.event
async def on_ready():
    print('Logged on as', client.user)
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.author == client.user or message.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_NEW,
           "message": {"id": message.id, "channel_id": message.channel.id, "user_id": message.author.id}}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)


@client.event
async def on_message_delete(message):
    if message.author == client.user or message.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_DELETE,
           "message": {"id": message.id, "channel_id": message.channel.id, "user_id": message.author.id}}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)


@client.event
async def on_message_edit(before, after):
    if after.author == client.user or after.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_EDIT,
           "message_old": {"id": before.id, "channel_id": before.channel.id, "user_id": before.author.id},
           "message": {"id": after.id, "channel_id": after.channel.id, "user_id": after.author.id}}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user or reaction.message.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.REACTION_ADD,
           "reaction": {"count": reaction.count, "me": reaction.me, "user_id": user.id,
            "message": {"id": reaction.message.id, "channel_id": reaction.message.channel.id,
            "user_id": reaction.message.author.id}, "emoji": await obj_from_emoji(reaction.emoji)}}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)


@client.event
async def on_reaction_remove(reaction, user):
    if user == client.user or reaction.message.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.REACTION_REMOVE,
           "reaction": {"count": reaction.count, "me": reaction.me, "user_id": user.id,
            "message": {"id": reaction.message.id, "channel_id": reaction.message.channel.id,
            "user_id": reaction.message.author.id}, "emoji": await obj_from_emoji(reaction.emoji)}}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)

client.run(confirmation_token)
