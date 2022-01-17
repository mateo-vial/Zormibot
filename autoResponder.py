import discord
from discord.ext import tasks
from discord.ext import commands
from tabulate import tabulate
import pickle
import os
import random
from copy import copy

from class_joueur import *
from class_date import *




prefix = '$'
lenprefix = len(prefix)

listecommandes = ['hello', 'help', 'ajouterjoueur', 'listejoueurs', 'supprimerjoueur', 'teps', 'swapjoueurs', 'exit']


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.bot.user))

    @commands.Cog.listener()
    async def on_message(self, message):
        # print('Message from {0.author} in channel id {0.channel.id} server id {0.guild.id} : {0.content}'.format(message))
        if message.author.id == self.bot.user.id:
            return

        # Mentions Zorm
        if 135495101496426496 in [user.id for user in message.mentions] and message.author.id != 135495101496426496:
            mention = message.author.mention
            await message.channel.send('{0}, ne dérange pas le boss.'.format(mention))

        # Bob l'éponge
        if message.author.id == 718534355210862734 and random.randrange(10) == 0:
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
        if not message.author.bot:
            rand_tg = random.randrange(180)
            if rand_tg == 1:
                await message.channel.send('Pitié ta gueule {0}'.format(message.author.name))

        # Feur
        if ''.join(c for c in message.content if c.isalpha()).lower().endswith('quoi'):
            await message.channel.send(file = discord.File('feur/' + random.choice(os.listdir('feur'))))

        
        nelist = ['né', 'nez', 'nait', 'ner', 'nés', 'née', 'nées', 'nais', 'naient', 'nai', 'ney']
        if any([''.join(c for c in message.content if c.isalpha()).lower().endswith(ne) for ne in nelist]):
            await message.channel.send('gro', delete_after = 60)

# Every extension should have this function
def setup(bot):
    bot.add_cog(MyCog(bot))