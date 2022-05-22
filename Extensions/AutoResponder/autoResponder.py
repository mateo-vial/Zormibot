import discord
from discord.ext import commands
import os
import random

from main import toggles

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        # print('Message from {0.author} in channel id {0.channel.id} server id {0.guild.id} : {0.content}'.format(message))
        if message.author.bot:
            return

        # tag
        if toggles['tag'] and 135495101496426496 in [user.id for user in message.mentions] and message.author.id != 135495101496426496:
            await message.channel.send('{0.author.name}, ne dérange pas le boss.'.format(message), delete_after=10)

        # Bob l'éponge
        if toggles['bobleponge'] and random.randrange(1200) == 0:
            output = ''
            for char in message.content:
                if random.randrange(2) == 0:
                    output += char.swapcase()
                else:
                    output += char
            await message.channel.send(output, file=discord.File('Assets/bob.jpg'), delete_after=10)

        # T'ecris bcp
        if toggles['tecrisbcp'] and len(message.content) > 200 and random.randrange(10) == 0:
            await message.channel.send(file=discord.File('Assets/tecrisbcp/' + random.choice(os.listdir('tecrisbcp'))), delete_after=10)

        # PTG
        if toggles['ptg'] and random.randrange(1000) == 0:
            await message.channel.send('Pitié ta gueule {0}'.format(message.author.name), delete_after=10)

        # Feur
        if toggles['feur'] and random.randrange(20) == 0 and ''.join(c for c in message.content if c.isalpha()).lower().endswith('quoi'):
            await message.channel.send(file=discord.File('Assets/feur/' + random.choice(os.listdir('feur'))), delete_after=10)
        
        
def setup(bot):
    bot.add_cog(MyCog(bot)) 