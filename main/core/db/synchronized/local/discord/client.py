# -*- coding: utf8 -*-

import main.core.db.synchronized.local.discord as home_dir
import discord

path = str(home_dir.__path__).replace('_NamespacePath([\'', '').replace('\'])', '')
with open(path + '/token.secret') as file:
    token = file.readline()
with open(path + '/client_id.secret') as file:
    client_id = file.readline()
with open(path + '/client_secret.secret') as file:
    client_secret = file.readline()


class DiscordClient:
    client = discord.Client()
    token = token
    client_id = client_id
    client_secret = client_secret
