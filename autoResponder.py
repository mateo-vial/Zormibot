import discord
from discord.ext import tasks
from discord.ext import commands
from tabulate import tabulate
import pickle
import os
import random
import datetime
from copy import copy

from class_joueur import *


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.bot.user))

    @commands.Cog.listener()
    async def on_message(self, message):

        rng = random.randrange(10000)

        # print('Message from {0.author} in channel id {0.channel.id} server id {0.guild.id} : {0.content}'.format(message))
        if message.author.id == self.bot.user.id:
            return

        # Mentions Zorm
        if 135495101496426496 in [user.id for user in message.mentions] and message.author.id != 135495101496426496:
            await message.channel.send('{0.author.name}, ne dérange pas le boss.'.format(message))

        # Bob l'éponge
        if rng<25:
            output = ''
            for char in message.content:
                if random.randrange(2) == 0:
                    output += char.swapcase()
                else:
                    output += char
            await message.channel.send(output, file = discord.File('bob.jpg'))

        # T'écris bcp
        if len(message.content) > 200:
            await message.channel.send(file = discord.File('tecrisbcp/' + random.choice(os.listdir('tecrisbcp'))))

        # PTG
        if not message.author.bot and rng<100:
            await message.channel.send('Pitié ta gueule {0}'.format(message.author.name))

        # Feur
        if ''.join(c for c in message.content if c.isalpha()).lower().endswith('quoi'):
            await message.channel.send(file = discord.File('feur/' + random.choice(os.listdir('feur'))))

        # Special
        nelist = ['né', 'nez', 'nait', 'ner', 'nés', 'née', 'nées', 'nais', 'naient', 'nai', 'ney']
        if any([''.join(c for c in message.content if c.isalpha()).lower().endswith(ne) for ne in nelist]):
            await message.channel.send('gro', delete_after = 60)

# Every extension should have this function
def setup(bot):
    bot.add_cog(MyCog(bot)) 