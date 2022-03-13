from discord.ext import commands

class autoReact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author.bot:
            return

        CHECK_BOX = "\U00002611"
        X_MARK = "\U0000274C"
        mots_popop = ['kick', 'popop']
        
        mots_zormibot = ['kick', 'zormibot']
        reac_X = [
            '\U0000274c', # cross mark
            '\U00002716', # multiplication
            '\U0001f1fd', # lettre x
            '\U00002753', # ?
            '\U00002049', # ?!
            '\U000026d4', # sens interdit
            '\U0001f6ab', # interdit
            '\U0001f6b7', # no piétons
            '\U0001f645', # geste non
            '\U0000274e', # croix verte
        ]

        if all(mot in message.content.lower().split() for mot in mots_popop):
            await message.add_reaction(CHECK_BOX)
        
        if all(mot in message.content.lower().split() for mot in mots_zormibot):
            for reac in reac_X:
                await message.add_reaction(reac)


def setup(bot):
    bot.add_cog(autoReact(bot))