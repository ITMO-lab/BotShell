import discord
import json
import pickle

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message_id = str(message.id)
    channel_id = str(message.channel.id)
    message_decoded = await client.get_channel(int(channel_id)).fetch_message(int(message_id))
    #discord.abc.Messageable().fetch_message(int(message_str))
    # message_decoded.channel = discord.DMChannel()
    # message_decoded.channel.id = message.channel.id
    # await message.channel.send(message.content)
    await message_decoded.channel.send(message.content)

import os
cur_dir = '/test_tree/discord_tests'
path = os.getcwd()
if path.count(cur_dir) != 0:
    path = path[:len(path) - len(cur_dir)] + '/main/core/event_handler/discord'
with open(path + '/token.secret') as file:
    confirmation_token = file.readline()
client.run(confirmation_token)
