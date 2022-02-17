import discord
from discord.ext import tasks
from discord.ext import commands
from tabulate import tabulate
import pickle
import os
import random
import datetime
from copy import copy

from class_joueur2 import Joueur2 as Joueur

random.seed()

pickle_filename = 'registre'
# si le fichier pickle n'existe pas, on réinitialise la listejoueurs. sinon, on le récupère
if not os.path.isfile(pickle_filename):
    listejoueurs = []
else:
    with open(pickle_filename, 'rb') as f:
        listejoueurs = pickle.load(f)

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
    'modifjoueur'
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
try:
    bot.load_extension("secret")
except:
    print("No secret extension available")

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
    await ctx.send(output, delete_after=30)

@bot.command(name='ajouterjoueur', aliases=['aj'])
async def ajouterjoueur(ctx, *args):
    assert ctx.author.id in adminlist
    assert ctx.channel.id in chancmdlist
    try:
        listejoueurs.append(Joueur(
            statut = args[0].lower(), #'M' ou 'S' ou 'm' ou 's'
            draps = args[1].split(','),
            pseudo = args[2],
            prenom = args[3],
            twitter = args[4],
            fc = args[5],
            anniv = datetime.date(year=int(args[6][4:8]), month=int(args[6][2:4]), day=int(args[6][0:2])),
            num = args[7],
            exteams = args[8].split(',')
        ))

        with open(pickle_filename, 'wb') as f:
            pickle.dump(listejoueurs, f)
        
        if args[2] == '/':
            pseud_temp = args[3]
        else:
            pseud_temp = args[2]
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
   # for joueur in listejoueurs:
    #    await ctx.send(joueur.affiche())

    for i in range((len(listejoueurs)+1) // 2):
        output = ''
        output += listejoueurs[2*i].affiche() 
        try:
            output += listejoueurs[2*i+1].affiche()
        except:
            pass
        await ctx.send(output)


@bot.command(name='listejoueurs', aliases=['lj'])
async def _listejoueurs(ctx): # underscore because listejoueurs is already the list of all players
    table = [['N°', 'Drapeaux', 'Pseudo', 'Prénom', 'Twitter', 'FC', 'Anniv', 'Num', 'Ex-teams']]
    for i, joueur in enumerate(listejoueurs):
        liste_temp = [i] 
        liste_temp += joueur.liste_affiche()
        table.append(liste_temp)
    output = tabulate(table, headers='firstrow', tablefmt='simple')
    try:
        await ctx.send('```{0}```'.format(output), delete_after=30)
    except: # if output too long
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

        with open(pickle_filename, 'wb') as f:
            pickle.dump(listejoueurs, f)

        await ctx.send('Joueurs {0} et {1} échangés.'.format(i, j), delete_after=10)
    except:
        await ctx.send('Usgae incorrect.', delete_after=10)

@bot.command(name='deplacejoueur', aliases=['dj'])
async def deplacejoueur(ctx, *args):
    assert ctx.author.id in adminlist
    assert ctx.channel.id in chancmdlist
    try:
        i, j = int(args[0]), int(args[1])
        joueur_temp = copy(listejoueurs[i])
        if listejoueurs[i].pseudo == None:
            pseud_temp = listejoueurs[i].prenom
        else:
            pseud_temp = listejoueurs[i].pseudo
        del listejoueurs[i]
        listejoueurs.insert(j, joueur_temp)

        with open(pickle_filename, 'wb') as f:
            pickle.dump(listejoueurs, f)

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

@bot.command(name='naissances')
async def naissances(ctx):
    # Initialisation du dictionnaire
    dict_annees = {}
    for joueur in listejoueurs:
        if joueur.anniv.year not in dict_annees:
            dict_annees[joueur.anniv.year] = [joueur]
        else:
            dict_annees[joueur.anniv.year].append(joueur)

    # Tri des valeurs du dictionnaire
    for annee in dict_annees:
        dict_annees[annee].sort(key = lambda joueur: joueur.anniv)

    # On génère l'affiche
    embed = discord.Embed(
        title=":baby: Naissances",  
        color=0xFF5733,
        type='rich'
    )
    for annee in sorted(dict_annees):
        embed.add_field(
            name=annee, 
            value='```{0}```'.format('\n'.join([joueur.pseudo+' ('+'{:02d}/{:02d}'.format(joueur.anniv.day, joueur.anniv.month)+')' for joueur in dict_annees[annee]])),
            inline=True
        )
    
    
    #output = ':baby: Naissances```{0}```'.format('\n'.join(['{0} : {1}'.format(annee, ' > '.join([joueur.pseudo+' ('+'{:02d}/{:02d}'.format(joueur.anniv.day, joueur.anniv.month)+')' for joueur in dict_annees[annee]])) for annee in sorted(dict_annees)]))
    
    #await ctx.send(output)
    await ctx.send(embed=embed)

@bot.command(name='anniversaires', aliases=['anniv'])
async def anniversaires(ctx):
    #Initialisation du dictionnaire
    liste_mois = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ]

    dict_mois = {}
    for i in range(12):
        dict_mois[i+1] = []
    
    # Remplissage du dictionnaire
    for joueur in listejoueurs:
        dict_mois[joueur.anniv.month].append(joueur)
    
    # Tri des valeurs du dictionnaire (On se base sur l'année 2004 pour prendre en compte les 29 février)
    for i in dict_mois:
        dict_mois[i].sort(key = lambda joueur: datetime.date(year=2004, month=joueur.anniv.month, day=joueur.anniv.day))
    
    # On génère l'affiche
    embed = discord.Embed(
        title=":birthday: Anniversaires",  
        color=0xFF5733,
        type='rich'
    )
    for i in dict_mois:
        embed.add_field(
            name=liste_mois[i-1],
            value='```{0}```'.format('\n'.join([joueur.pseudo+' ('+str(joueur.anniv.day)+')' for joueur in dict_mois[i]])),
            inline=True
        )
    await ctx.send(embed=embed)

    #output = ':birthday: Anniversaires```\n{0}```'.format('\n'.join([' '*(9-len(liste_mois[i-1]))+liste_mois[i-1]+' : '+', '.join([joueur.pseudo+' ('+str(joueur.anniv.day)+')' for joueur in dict_mois[i]]) for i in dict_mois]))
    #await ctx.send(output)

@bot.command(name='fc')
async def fc(ctx, *args):
    table = [['N°', 'Pseudo', 'FC']]
    if len(args)>=1:
        for i, joueur in enumerate(listejoueurs):
            if joueur.pseudo.lower() in [arg.lower() for arg in args]:
                table.append([i, joueur.pseudo, 'SW-'+'-'.join([joueur.fc[0:4], joueur.fc[4:8], joueur.fc[8:12]])])
    elif len(args)==0:
        for i, joueur in enumerate(listejoueurs):
            table.append([i, joueur.pseudo, 'SW-'+'-'.join([joueur.fc[0:4], joueur.fc[4:8], joueur.fc[8:12]])])
    if len(table)==1:
        await ctx.send('Pseudo introuvable.')
        return
    output = tabulate(table, headers='firstrow', tablefmt='simple')
    await ctx.send('```{0}```'.format(output), delete_after=30)

@bot.command(name='modifjoueur', aliases=['mj'])
async def modifjoueur(ctx, *args):
    try:
        assert args[1] in ['statut', 'draps', 'prenom', 'pseudo', 'twitter', 'fc', 'anniv', 'num', 'exteams']
        i = int(args[0])
        if args[1] in ['draps', 'exteams']:
            setattr(listejoueurs[i], args[1], args[2].split(','))
        elif args[1] == 'anniv':
            setattr(
                listejoueurs[i], 
                args[1], 
                datetime.date(
                    year=int(args[2][4:8]), 
                    month=int(args[2][2:4]), 
                    day=int(args[2][0:2])
                )
            )
        elif args[1] == 'statut':
            setattr(listejoueurs[i], args[1], args[2].lower())
        else:
            setattr(listejoueurs[i], args[1], args[2])

        with open(pickle_filename, 'wb') as f:
            pickle.dump(listejoueurs, f)

        await ctx.send('{0} de {1} modifié'.format(args[1], listejoueurs[i].pseudo))
    except:
        await ctx.send('Usage incorrect', delete_after=30)


@bot.command(name='test')
async def embed(ctx):
    embed=discord.Embed(
        title="Liste des joueurs",   
        color=0xFF5733,
        type='rich'
    )
    for i in range((len(listejoueurs)+1)//2):
        j1 = listejoueurs[2*i]
        j2 = listejoueurs[2*i+1]
        embed.add_field(name=j1.affiche_title_embed(), value=j1.affiche_value_embed(), inline=True)
        try: embed.add_field(name=j2.affiche_title_embed(), value=j2.affiche_value_embed(), inline=True) 
        except: pass
        embed.add_field(name='\u200b', value='\u200b', inline=False)
    await ctx.send(embed=embed)

@bot.command(name='test2')
async def embed(ctx):
    embed=discord.Embed(
        title="Liste des joueurs",  
        description="Bah c'est la liste des joueurs quoi", 
        color=0xFF5733,
        type='rich'
    )
    for j in listejoueurs[:24]:
        embed.add_field(name=j.affiche_title_embed(), value=j.affiche_value_embed(), inline=True)
    await ctx.send(embed=embed)
    if len(listejoueurs)>24:
        embed=discord.Embed( 
        color=0xFF5733,
        type='rich'
        )
        for j in listejoueurs[24:]:
            embed.add_field(name=j.affiche_title_embed(), value=j.affiche_value_embed(), inline=True)
        
        await ctx.send(embed=embed)

bot.run(TOKEN)


