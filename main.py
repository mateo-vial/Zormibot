import discord
from discord.ext import tasks
from discord.ext import commands
from tabulate import tabulate
import pickle
import os
import random
import datetime
from copy import copy
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from class_joueur import Joueur

random.seed()
pickle_filename = 'registre'
counter_table_filename = 'counter_table'


# -------------------------------------------------------- #
# RECUPERATION DU FICHIER PICKLE POUR LA LISTE DES JOUEURS #
# et aussi du counter :)                                   #
# -------------------------------------------------------- #
if not os.path.isfile(pickle_filename):
    listejoueurs = []
else:
    with open(pickle_filename, 'rb') as f:
        listejoueurs = pickle.load(f)

if not os.path.isfile(counter_table_filename):
    counter_table = [[0,0,0],[0,0,0]]
else:
    with open(counter_table_filename, 'rb') as f:
        counter_table = pickle.load(f)
print('compteur réglé à ', counter_table)


bot = commands.Bot(command_prefix="$",  help_command=None)

listecommandes = [
    'hello', 
    'help', 
    'ajouterjoueur', 
    'listejoueurs', 
    'supprimerjoueur', 
    'deplacejoueur',
    'teps', 
    'swapjoueurs', 
    'stop',
    'naissances',
    'anniversaires',
    'fc',
    'modifjoueur',
    'tl'
]
 
# ------------------------------------------------------- #
# RECUPERATION DES FICHIERS ADMIN ET CHANCOMMAND ET TOKEN #
# ------------------------------------------------------- #
with open('admin.txt', mode='r', encoding='utf-8') as f:
    adminlist = [int(line.split()[0]) for line in f.readlines()]
    # edit admin.txt to edit admins
with open('chancmd.txt', mode='r', encoding='utf-8') as f:
    chancmdlist = [int(line.split()[0]) for line in f.readlines()]
    # edit chancmd.txt to edit channels
with open("token.txt", "r") as f:
    TOKEN = f.read()
    # token.txt


# ----------------------------- #
#          BOT LAUNCH           #
# ----------------------------- #
@bot.event
async def on_ready():
    print("Le bot est prêt.")

bot.load_extension("autoResponder")
try:
    bot.load_extension("secret")
except:
    print("No secret extension available")

# ----------------------------- #
#          EXTENSIONS           #
# ----------------------------- #
cogs_dir = 'Cogs'
cogs_list = [f for f in os.listdir(cogs_dir) if f.endswith('.py')]
print('extensions : ')
print(cogs_list)
for cog in cogs_list:
    bot.load_extension(cogs_dir + '.' + cog[:-3])





@bot.command(name='help')
async def help(ctx, *args):
    if len(args) == 0:
        output = '```'
        for cmd in listecommandes:
            output += '{0}{1}\n'.format(bot.command_prefix, cmd)
        output += '```'
    elif len(args) >= 1:
        try:
            with open('help/{0}.txt'.format(args[0]), encoding='utf-8') as f:
                output = '```{0}```'.format(f.read().format(bot.command_prefix))
        except:
            output = '''Cette commande n'existe pas.'''
    await ctx.send(output, delete_after=30)

bot.run(TOKEN)


