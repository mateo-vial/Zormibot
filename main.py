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

random.seed()




intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("Le bot est prêt.")

# Put locally your token in a file named token.txt
# It won't be upload on github due to gitignore 
with open("token.txt", "r") as f:
    TOKEN = f.read()
bot.load_extension("autoResponder")
bot.run(TOKEN)


