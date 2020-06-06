# -*- coding: utf8 -*-

data = "<Message id=718820557692600341 channel=<DMChannel id=718416701603053659 recipient=<User id=194426461229285376 name='Жидков Артемий' discriminator='4076' bot=False>> type=<MessageType.default: 0> author=<User id=194426461229285376 name='Жидков Артемий' discriminator='4076' bot=False> flags=<MessageFlags value=0>>"

import discord

msg = discord.Message()
msg.channel = discord.DMChannel()
