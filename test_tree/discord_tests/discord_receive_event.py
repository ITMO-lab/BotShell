# -*- coding: utf8 -*-

import discord

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
    await message.channel.send(f'on_message {str(message)}')


@client.event
async def on_message_delete(message):
    if message.author == client.user or message.channel.type != discord.ChannelType.private:
        return
    await message.channel.send(f'on_message_delete {str(message)}')


@client.event
async def on_message_edit(before, after):
    if after.author == client.user or after.channel.type != discord.ChannelType.private:
        return
    await after.channel.send(f'on_message_edit {str(after)}')


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user or reaction.message.channel.type != discord.ChannelType.private:
        return
    await reaction.message.channel.send(f'on_reaction_add {str(reaction)}')


@client.event
async def on_reaction_remove(reaction, user):
    if user == client.user or reaction.message.channel.type != discord.ChannelType.private:
        return
    await reaction.message.channel.send(f'on_reaction_remove {str(reaction)}')


import os
cur_dir = '/main/core/event_handler/discord'
path = os.getcwd()
if path.count(cur_dir) == 0:
    path += '/../..' + cur_dir
with open(path + '/token.secret') as file:
    confirmation_token = file.readline()
client.run(confirmation_token)
