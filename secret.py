import discord
from discord.ext import tasks
from discord.ext import commands
from tabulate import tabulate
import pickle
import os
import random
import datetime
from copy import copy

#from class_joueur import *


class Secret(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Every extension should have this function
def setup(bot):
    bot.add_cog(Secret(bot)) 