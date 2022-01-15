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


pickle_filename = 'registre'

# si le fichier pickle n'existe pas, on réinitialise la listejoueurs. sinon, on le récupère
if not os.path.isfile(pickle_filename):
    listejoueurs = []
else:
    file = open(pickle_filename, 'rb')
    listejoueurs = pickle.load(file)

prefix = '$'
lenprefix = len(prefix)

listecommandes = ['hello', 'help', 'ajouterjoueur', 'listejoueurs', 'supprimerjoueur', 'teps', 'swapjoueurs', 'exit']


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.bot.user))

    @commands.Cog.listener()
    async def on_message(self, message):
        # print('Message from {0.author} in channel id {0.channel.id} server id {0.guild.id} : {0.content}'.format(message))
        if message.author.id == self.bot.user.id:
            return

        # Mentions Zorm
        if 135495101496426496 in [user.id for user in message.mentions] and message.author.id != 135495101496426496:
            mention = message.author.mention
            await message.channel.send('{0}, ne dérange pas le boss.'.format(mention))

        # Bob l'éponge
        if message.author.id == 718534355210862734 and random.randrange(10) == 0:
            output = ''
            for char in message.content:
                if random.randrange(2) == 0:
                    output += char.swapcase()
                else:
                    output += char
            await message.channel.send(output, file = discord.File('bob.jpg'))

        # T'écris bcp
        if len(message.content) > 200:
            await message.channel.send(file = discord.File('tecrisbcp/' + random.choice(os.listdir('tecrisbcp'))))

        # PTG
        if not message.author.bot:
            rand_tg = random.randrange(180)
            if rand_tg == 1:
                await message.channel.send('Pitié ta gueule {0}'.format(message.author.name))

        # Feur
        if ''.join(c for c in message.content if c.isalpha()).lower().endswith('quoi'):
            await message.channel.send(file = discord.File('feur/' + random.choice(os.listdir('feur'))))

        
        nelist = ['né', 'nez', 'nait', 'ner', 'nés', 'née', 'nées', 'nais', 'naient', 'nai', 'ney']
        if any([''.join(c for c in message.content if c.isalpha()).lower().endswith(ne) for ne in nelist]):
            await message.channel.send('gro', delete_after = 60)

        

        # removed for my tests
        # assert message.channel.id in [814185273936052284, 930934616485949500]

        if message.content.startswith(prefix):
            mots = message.content[lenprefix:].split()

            if mots[0] == 'hello':
                await message.channel.send('Hello world!', delete_after = 5)
            
            elif mots[0] == 'help':
                if len(mots) == 1:
                    output = 'Liste des commandes :\n```' + '\n'.join([prefix + cmd for cmd in listecommandes]) + """```\nPour de l'aide sur une commande particulière, ``{0}help <commande>``""".format(prefix)
                    await message.channel.send(output, delete_after = 30)
                elif len(mots) == 2:
                    try:
                        output = open('help/{0}.txt'.format(mots[1]), mode = 'r', encoding = 'utf-8').read()
                        await message.channel.send('```{0}```'.format(output.format(prefix)), delete_after = 30)
                    except:
                        await message.channel.send("""Cette commande n'existe pas.""", delete_after = 10)         
                else:
                    output = 'Usage incorrect.\n```{0}help\n{0}help <commande>```'.format(prefix)                

            elif mots[0] in  ['ajouterjoueur', 'aj']:
                if len(mots) != 9:
                    # output = 'Usage incorrect.\n```{0}ajouterjoueur <pseudo>```'.format(prefix)
                    output = 'Usage incorrect.\n```$ajouterjoueur <draps> <pseudo> <prénom> <twitter> <fc> <anniv> <num> <exteams>```'
                    await message.channel.send(output, delete_after = 20)
                else:
                    listejoueurs.append(Joueur(
                        draps = mots[1].split(','),
                        pseudo = mots[2],
                        prenom = mots[3],
                        twitter = mots[4],
                        fc = mots[5],
                        anniv = Date(annee = int(mots[6][4:8]), mois = int(mots[6][2:4]), jour = int(mots[6][0:2])),
                        num = mots[7],
                        exteams = mots[8].split(','),                    
                    ))

                    file = open(pickle_filename, 'wb')
                    pickle.dump(listejoueurs, file)

                    if mots[2] == '/':
                        pseud_temp = mots[3]
                    else:
                        pseud_temp = mots[2]

                    await message.channel.send('Joueur {0} ajouté au registre.'.format(pseud_temp), delete_after = 8)

            elif mots[0] in ['supprimerjoueur', 'sj']:
                if len(mots) != 2:
                    output = 'Usage incorrect.\n```{0}supprimerjoueur <N°>```'.format(prefix)
                    await message.channel.send(output, delete_after = 20)
                else:
                    try:
                        id_a_supprimer = int(mots[1]) # peut avoir une erreur
                        if listejoueurs[id_a_supprimer].pseudo == None:
                            pseud_temp = listejoueurs[id_a_supprimer].prenom
                        else:
                            pseud_temp = listejoueurs[id_a_supprimer].pseudo
                        del listejoueurs[id_a_supprimer]

                        file = open(pickle_filename, 'wb')
                        pickle.dump(listejoueurs, file)

                        await message.channel.send('Joueur {0} supprimé du registre.'.format(pseud_temp), delete_after = 8)
                        await message.channel.send("""Les N° sont modifiés après la suppression d'un joueur.""", delete_after = 8)
                    except:
                        output = 'Usage incorrect.\n```{0}supprimerjoueur <N°>```'.format(prefix)
                        await message.channel.send(output, delete_after = 20)

            elif mots[0] == 'affiche':

                for joueur in listejoueurs:
                    await message.channel.send(joueur.affiche())

            elif mots[0] in ['listejoueurs', 'lj']:
                table = [['N°', 'Drapeaux', 'Pseudo', 'Prénom', 'Twitter', 'FC', 'Anniv', 'Num', 'Ex-teams']]
                for i, joueur in enumerate(listejoueurs):
                    liste_temp = [i]
                    liste_temp += joueur.liste_affiche()
                    table.append(liste_temp)
                output = tabulate(table, headers="firstrow", tablefmt="simple")
                try:
                    await message.channel.send('```{0}```'.format(output), delete_after = 30)
                except:
                    if os.path.isfile('lj.txt'):
                        os.remove('lj.txt')
                    f = open('lj.txt', mode = 'w', encoding = 'utf-8')
                    f.write(output)
                    f.close()
                    await message.channel.send(file = discord.File('lj.txt'), delete_after = 30)

            elif mots[0] in ['swapjoueurs', 'swapj']:
                if len(mots) == 3:
                    try:
                        i, j = int(mots[1]), int(mots[2])
                        listejoueurs[i], listejoueurs[j] = listejoueurs[j], listejoueurs[i]
                        await message.channel.send('Joueurs {0} et {1} échangés.'.format(i,j), delete_after = 8)
                    except:
                        await message.channel.send('Usage incorrect.', delete_after = 8)

            elif mots[0] in ['deplacejoueur', 'deplacej']:
                if len(mots) == 3:
                    try:
                        i, j = int(mots[1]), int(mots[2])
                        joueur_temp = copy(listejoueurs[i])
                        pseud_temp = listejoueurs[i].pseudo
                        del listejoueurs[i]
                        listejoueurs.insert(j, joueur_temp)
                        await message.channel.send("""Joueur {0} déplacé à l'emplacement {1}""".format(pseud_temp, j), delete_after = 8)
                    except:
                        await message.channel.send('Usage incorrect.', delete_after = 8)
                        
            elif mots[0] == 'teps':
                await message.channel.send(file = discord.File(random.choice(['prout/{0}'.format(file) for file in os.listdir('prout') if os.path.isfile('prout/{0}'.format(file))])), delete_after = 8)

            elif mots[0] == 'stop' and message.author.id == 135495101496426496:
                await message.channel.send('Ciao.')
                exit()

            else:
                await message.channel.send('Commande inconnue. Tapez ``{0}help`` pour voir la liste des commandes.'.format(prefix), delete_after = 8)

# Every extension should have this function
def setup(bot):
    bot.add_cog(MyCog(bot))