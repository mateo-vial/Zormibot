import discord
from discord.ext import commands

from main import toggles

class Chatting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 297752161377583116 and toggles['chatting']:
            content = message.content
            emote = '<a:chatting:967485297514397716>'
            await message.channel.send('''{0} "{1}"'''.format(emote, content))

def setup(bot):
    bot.add_cog(Chatting(bot))