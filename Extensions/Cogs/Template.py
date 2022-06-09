import discord
from discord.ext import commands

class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def cmd1(self, ctx, *args):
        await ctx.send('Commande test. Arguments : {0}. Delete after 5.'.format(args), delete_after=5)


def setup(bot):
    bot.add_cog(Template(bot))