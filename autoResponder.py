import discord
from discord.ext import tasks
from discord.ext import commands
from tabulate import tabulate
import pickle
import os
import random
import datetime
from copy import copy


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        # print('Message from {0.author} in channel id {0.channel.id} server id {0.guild.id} : {0.content}'.format(message))
        if message.author.bot:
            return

        # Mentions 
        if 135495101496426496 in [user.id for user in message.mentions] and message.author.id != 135495101496426496:
            await message.channel.send('{0.author.name}, ne dérange pas le boss.'.format(message),delete_after=10)

        # Bob l'éponge
        if random.randrange(300) == 0 and False:
            output = ''
            for char in message.content:
                if random.randrange(2) == 0:
                    output += char.swapcase()
                else:
                    output += char
            await message.channel.send(output, file = discord.File('bob.jpg'),delete_after=10)

        # T'écris bcp
        if len(message.content) > 200:
            await message.channel.send(file = discord.File('tecrisbcp/' + random.choice(os.listdir('tecrisbcp'))), delete_after=10)

        # PTG
        if random.randrange(700) == 0:
            await message.channel.send('Pitié ta gueule {0}'.format(message.author.name), delete_after=10)

        # Feur
        if False and ''.join(c for c in message.content if c.isalpha()).lower().endswith('quoi'):
            await message.channel.send(file = discord.File('feur/' + random.choice(os.listdir('feur'))),delete_after=10)

        # ftg popop
        if message.author.id == 847888116848001044 and False:
            await message.delete()
            await message.channel.send('ferme ta gueule popop jen ai marre de toi', delete_after=10)
       


        

# Every extension should have this function
def setup(bot):
    bot.add_cog(MyCog(bot)) 