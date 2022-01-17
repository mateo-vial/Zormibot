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

pickle_filename = 'registre'
# si le fichier pickle n'existe pas, on réinitialise la listejoueurs. sinon, on le récupère
if not os.path.isfile(pickle_filename):
    listejoueurs = []
else:
    file = open(pickle_filename, 'rb')
    listejoueurs = pickle.load(file)

bot = commands.Bot(command_prefix="$",  help_command=None)

listecommandes = [
    'hello', 
    'help', 
    'ajouterjoueur', 
    'listejoueurs', 
    'supprimerjoueur', 
    'teps', 
    'swapjoueurs', 
    'exit'
]

with open('admin.txt', mode='r', encoding='utf-8') as f:
    adminlist = [int(line.split()[0]) for line in f.readlines()]
    # edit admin.txt to edit admins

with open('chancmd.txt', mode='r', encoding='utf-8') as f:
    chancmdlist = [int(line.split()[0]) for line in f.readlines()]
    # edit chancmd.txt to edit channels

@bot.event
async def on_ready():
    print("Le bot est prêt.")

# Put locally your token in a file named token.txt
# It won't be upload on github due to gitignore 
with open("token.txt", "r") as f:
    TOKEN = f.read()

bot.load_extension("autoResponder")

# All commands

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello world!')

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
    await ctx.send(output)

@bot.command(name='ajouterjoueur', aliases=['aj'])
async def ajouterjoueur(ctx, *args):
    assert ctx.author.id in adminlist
    assert ctx.channel.id in chancmdlist
    # await ctx.send('commande ajouterjoueur lancée')
    try:
        listejoueurs.append(Joueur(
            draps = args[0].split(','),
            pseudo = args[1],
            prenom = args[2],
            twitter = args[3],
            fc = args[4],
            anniv = Date(annee = int(args[5][4:8]), mois = int(args[5][2:4]), jour = int(args[5][0:2])),
            num = args[6],
            exteams = args[7].split(',')
        ))

        with open(pickle_filename, 'wb') as f:
            pickle.dump(listejoueurs, f)
        
        if args[1] == '/':
            pseud_temp = args[2]
        else:
            pseud_temp = args[1]
        await ctx.send('Joueur {0} ajouté au registre.'.format(pseud_temp), delete_after=10)
    except:
        await ctx.send('Usage incorrect', delete_after=10)

@bot.command(name='supprimerjoueur', aliases=['sj'])
async def supprimerjoueur(ctx, arg):
    assert ctx.author.id in adminlist
    assert ctx.channel.id in chancmdlist
    try:
        ind_a_supprimer = int(arg)
        if listejoueurs[ind_a_supprimer].pseudo == None:
            pseud_temp = listejoueurs[ind_a_supprimer].prenom
        else:
            pseud_temp = listejoueurs[ind_a_supprimer].pseudo
        del listejoueurs[ind_a_supprimer]

        with open(pickle_filename, 'wb') as f:
            pickle.dump(listejoueurs, f)

        await ctx.send('''Joueur {0} supprimé du registre.\n Les N° sont modifiés après la suppression d'un joueur.'''.format(pseud_temp), delete_after = 10)
    except:
        await ctx.send('Usage incorrecte', delete_after=10)

@bot.command(name='affiche')
async def affiche(ctx):
    for joueur in listejoueurs:
        await ctx.send(joueur.affiche())

@bot.command(name='listejoueurs', aliases=['lj'])
async def _listejoueurs(ctx): #underscore because listejoueurs is already the list of all players
    table = [['N°', 'Drapeaux', 'Pseudo', 'Prénom', 'Twitter', 'FC', 'Anniv', 'Num', 'Ex-teams']]
    for i, joueur in enumerate(listejoueurs):
        liste_temp = [i] 
        liste_temp += joueur.liste_affiche()
        table.append(liste_temp)
    output = tabulate(table, headers='firstrow', tablefmt='simple')
    try:
        await ctx.send('```{0}```'.format(output), delete_after=30)
    except: # If output > 2000 or whatever 
        if os.path.isfile('lj.txt'):
            os.remove('lj.txt')
        with open('lj.txt', mode='w', encoding='utf-8') as f:
            f.write(output)
        await ctx.send(file=discord.File('lj.txt'), delete_after=30)

@bot.command(name='swapjoueurs', aliases=['swapj'])
async def swapjoueurs(ctx, *args):
    assert ctx.channel.id in chancmdlist
    assert ctx.author.id in adminlist
    try:
        i, j = int(args[0]), int(args[1])
        listejoueurs[i], listejoueurs[j] = listejoueurs[j], listejoueurs[i]
        await ctx.send('Joueurs {0} et {1} échangés.'.format(i, j), delete_after=10)
    except:
        await ctx.send('Usgae incorrect.', delete_after=10)

@bot.command(name='deplacejoueur', aliases=['dj'])
async def deplacejoueur(ctx, *args):
    assert ctx.author.id in adminlist
    assert ctx.channel.id in chancmdlist
    try:
        # await ctx.send('deplacejoueur en cours')
        i, j = int(args[0]), int(args[1])
        joueur_temp = copy(listejoueurs[i])
        if listejoueurs[i].pseudo == None:
            pseud_temp = listejoueurs[i].prenom
        else:
            pseud_temp = listejoueurs[i].pseudo
        del listejoueurs[i]
        listejoueurs.insert(j, joueur_temp)
        await ctx.send('''Joueur {0} déplacé à l'emplacement {1}'''.format(pseud_temp, j), delete_after=10)
    except:
        await ctx.send('Usage incorrect.', delete_after=10)

@bot.command(name='teps')
async def teps(ctx):
    await ctx.send(file = discord.File(random.choice(['prout/{0}'.format(file) for file in os.listdir('prout')])), delete_after = 10)

@bot.command(name='stop')
async def stop(ctx):
    assert ctx.author.id in adminlist
    await ctx.send('Ciao.')
    exit()


bot.run(TOKEN)


