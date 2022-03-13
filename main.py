from discord.ext import commands
import pickle
import os
import re
import random

random.seed(3)




# -------------------------------------------------------- #
# RECUPERATION DU FICHIER PICKLE POUR LA LISTE DES JOUEURS #
# et aussi du counter :)                                   #
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
    'startwar'
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
with open('token.txt', 'r') as f:
    TOKEN = f.read()
    # token.txt



# ----------------------------- #
#          BOT LAUNCH           #
# ----------------------------- #

bot = commands.Bot(command_prefix='$',  help_command=None)

@bot.event
async def on_ready():
    print('Le bot est prêt.')
   
#Unmute Zorm
#@bot.event
#async def on_voice_state_update(member, before, after):
#    if member.id == 135495101496426496:
#        if after.mute:
#            await member.edit(mute=False)

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
            with open('help/{0}.txt'.format(args[0]), encoding='utf-8') as f:
                output = '```{0}```'.format(f.read().format(bot.command_prefix))
        except:
            output = '''Cette commande n'existe pas.'''
    await ctx.send(output, delete_after=30)


bot.run(TOKEN)


