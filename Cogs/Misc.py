import discord
from discord.ext import commands
import random
import os

from main import adminlist, chancmdlist

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send('Hello world!')

    @commands.command(name='teps')
    async def teps(self, ctx):
        await ctx.send(
            file = discord.File(random.choice(['prout/{0}'.format(file) for file in os.listdir('prout')])), 
            delete_after = 10
        )
    
    @commands.command(name='stop')
    async def stop(self, ctx):
        assert ctx.author.id in adminlist
        await ctx.send('Ciao.')
        exit()

def setup(bot):
    bot.add_cog(Misc(bot))