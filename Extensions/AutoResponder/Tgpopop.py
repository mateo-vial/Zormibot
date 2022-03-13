from discord.ext import commands

class ftgpopop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 847888116848001044 and False:
            await message.delete()
            await message.channel.send('Ta gueule POPOP.', delete_after=10)


def setup(bot):
    bot.add_cog(ftgpopop(bot))