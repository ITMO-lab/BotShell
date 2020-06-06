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

client = discord.Client()


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
    ctx = {"type": EventType.MESSAGE_NEW, "message": message}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)


@client.event
async def on_message_delete(message):
    if message.author == client.user or message.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_DELETE, "message": message}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)


@client.event
async def on_message_edit(before, after):
    if after.author == client.user or after.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_EDIT, "before": before, "after": after}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user or reaction.message.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_EDIT, "reaction": reaction, "user": user}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)


@client.event
async def on_reaction_remove(reaction, user):
    if user == client.user or reaction.message.channel.type != discord.ChannelType.private:
        return
    ctx = {"type": EventType.MESSAGE_EDIT, "reaction": reaction, "user": user}
    event_handler.apply_async(args=(ctx,), queue='events', priority=5)

client.run(confirmation_token)
