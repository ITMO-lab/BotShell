import discord
import json
import pickle

global client
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
    await message_decoded.channel.send(message.content)


import main.core.db.synchronized.local.discord as home_dir
path = str(home_dir.__path__).replace('_NamespacePath([\'', '').replace('\'])', '')
with open(path + '/token.secret') as file:
    confirmation_token = file.readline()

client.run(confirmation_token)
