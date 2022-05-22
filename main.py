from discord.ext import commands
import pickle
import os
import re
import random

random.seed(3)




# -------------------------------------------------------- #
# RECUPERATION DU FICHIER PICKLE POUR LA LISTE DES JOUEURS #
# et aussi du counter :)                                   #
# + variables                                              #
# -------------------------------------------------------- #

listejoueurs_filename = 'pickles/listejoueurs'
counter_table_filename = 'pickles/counter_table'

def file_load(filename, default_value):
    if not os.path.isfile(filename):
        return default_value
    else:
        with open(filename, 'rb') as f:
            return pickle.load(f)

listejoueurs = file_load(listejoueurs_filename, default_value=[])
counter_table = file_load(counter_table_filename, default_value=[[0, 0, 0], [0, 0, 0], 0])


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
    'tl',
    'submit',
    'startwar',
    'toggle'
]

toggles = {'tag': False, 'bobleponge': False, 'tecrisbcp': False, 'ptg': False, 'feur': False, 'ne': False, 'chatting': False}

 
# ------------------------------------------------------- #
# RECUPERATION DES FICHIERS ADMIN ET CHANCOMMAND ET TOKEN #
# ------------------------------------------------------- #

with open('text_files/admin.txt', mode='r', encoding='utf-8') as f:
    adminlist = [int(line.split()[0]) for line in f.readlines()]
    # edit admin.txt to edit admins
with open('text_files/chancmd.txt', mode='r', encoding='utf-8') as f:
    chancmdlist = [int(line.split()[0]) for line in f.readlines()]
    # edit chancmd.txt to edit channels
with open('text_files/token.txt', 'r') as f:
    TOKEN = f.read()
    # token.txt



# ----------------------------- #
#          BOT DEFINE           #
# ----------------------------- #

bot = commands.Bot(command_prefix='$',  help_command=None)

@bot.event
async def on_ready():
    print('Le bot est prêt.')

# ----------------------------- #
#          EXTENSIONS           #
# ----------------------------- #

for (path, dirs, files) in os.walk('Extensions'):
    for file in files:
        if file.endswith('.py'):
            extension_name = re.sub('/|\\\\', '.', path) + '.' + file[:-3]
            bot.load_extension(extension_name)

# ------------------------- #
#       SOME COMMANDS       #
# ------------------------- #

@bot.command()
async def help(ctx, *args):
    if len(args) == 0:
        output = '```'
        for cmd in listecommandes:
            output += '{0}{1}\n'.format(bot.command_prefix, cmd)
        output += '```'
    elif len(args) >= 1:
        try:
            with open('Assets/help/{0}.txt'.format(args[0]), encoding='utf-8') as f:
                output = '```{0}```'.format(f.read().format(bot.command_prefix))
        except:
            output = '''Cette commande n'existe pas.'''
    await ctx.send(output, delete_after=30)


# pip install -U git+https://github.com/Rapptz/discord.py
# pip install -U discord.py==1.7.3

bot.run(TOKEN)


