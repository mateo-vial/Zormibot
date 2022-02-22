import discord
from discord.ext import commands
import datetime
import pickle
from tabulate import tabulate
from copy import copy
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from main import adminlist, chancmdlist, listejoueurs, pickle_filename
from class_joueur import Joueur as Joueur

def alias_to_ind(alias):
    """
    Retourne l'indice du (ou des) joueur(s) dont l'alias input figure dans l'attribut alias
    """
    try: 
        return [int(alias)] # if alias is a number in a string
    except: 
        return [i for i, joueur in enumerate(listejoueurs) if alias.lower() in [a.lower() for a in joueur.alias]]

class Joueurs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ajouterjoueur', aliases=['aj'])
    async def ajouterjoueur(self, ctx, statut, draps, pseudo, prenom, twitter, fc, anniv, num, exteams):
        assert ctx.author.id in adminlist
        assert ctx.channel.id in chancmdlist
        try:
            listejoueurs.append(Joueur(
                statut = statut.lower(), #'M' ou 'S' ou 'm' ou 's'
                draps = draps.split(','),
                pseudo = pseudo,
                prenom = prenom,
                twitter = twitter,
                fc = fc,
                anniv = datetime.date(year=int(anniv[4:8]), month=int(anniv[2:4]), day=int(anniv[0:2])),
                num = num,
                exteams = exteams.split(',')
            ))

            with open(pickle_filename, 'wb') as f:
                pickle.dump(listejoueurs, f)
        
            if pseudo == '/':
                pseud_temp = prenom
            else:
                pseud_temp = pseudo
            await ctx.send('Joueur {0} ajouté au registre.'.format(pseud_temp), delete_after=10)
        except:
            await ctx.send('Usage incorrect', delete_after=10)

    @commands.command(name='supprimerjoueur', aliases=['sj'])
    async def supprimerjoueur2(self, ctx, alias):
        assert ctx.author.id in adminlist
        assert ctx.channel.id in chancmdlist
        try:
            ind_a_supprimer = alias_to_ind(alias)[0]

            if listejoueurs[ind_a_supprimer].pseudo == None:
                pseud_temp = listejoueurs[ind_a_supprimer].prenom
            else:
                pseud_temp = listejoueurs[ind_a_supprimer].pseudo

            del listejoueurs[ind_a_supprimer]

            with open(pickle_filename, 'wb') as f:
                pickle.dump(listejoueurs, f)

            await ctx.send('''Joueur {0} supprimé du registre.\n (Les N° sont modifiés après la suppression d'un joueur)'''.format(pseud_temp), delete_after = 10)
        except:
            await ctx.send('Usage incorrecte', delete_after=10)

    @commands.command(name='listejoueurs', aliases=['lj'])
    async def listejoueurs_(self, ctx): # underscore because listejoueurs is already the list of all players
        table = [['N°', 'Statut', 'Drapeaux', 'Pseudo', 'Prénom', 'Twitter', 'FC', 'Anniv', 'Num', 'Ex-teams']]
        for i, joueur in enumerate(listejoueurs):
            liste_temp = [i] 
            liste_temp += joueur.liste_affiche()
            table.append(liste_temp)
        output = tabulate(table, headers='firstrow', tablefmt='simple')
    
        try:
            await ctx.send('```{0}```'.format(output), delete_after=30)
        except: # if output too long
            k = 15
            lines = output.split('\n')
            lines = ['\n'.join(lines[i:i+k]) for i in range(0,len(lines),k)]
            for line in lines:
                await ctx.send('```{0}```'.format(line),delete_after=30)

    @commands.command(name='affiche')
    async def affiche(self, ctx):
        for i in range((len(listejoueurs)+1) // 2):
            output = ''
            output += listejoueurs[2*i].affiche() 
            try:
                output += listejoueurs[2*i+1].affiche()
            except:
                pass
            await ctx.send(output)

    @commands.command(name='swapjoueurs', aliases=['swapj'])
    async def swapjoueurs(self, ctx, i, j):
        assert ctx.channel.id in chancmdlist
        assert ctx.author.id in adminlist
        try:
            i, j = int(i), int(j)
            listejoueurs[i], listejoueurs[j] = listejoueurs[j], listejoueurs[i]

            with open(pickle_filename, 'wb') as f:
                pickle.dump(listejoueurs, f)

            await ctx.send('Joueurs {0} et {1} échangés.'.format(i, j), delete_after=10)
        except:
            await ctx.send('Usgae incorrect.', delete_after=10)

    @commands.command(name='deplacejoueur', aliases=['dj'])
    async def deplacejoueur(self, ctx, alias, j):
        assert ctx.author.id in adminlist
        assert ctx.channel.id in chancmdlist
        try:
            i, j = alias_to_ind(alias)[0], int(j)
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

    @commands.command(name='naissances')
    async def naissances(self, ctx):
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
        await ctx.send(embed=embed)

    @commands.command(name='anniversaires', aliases=['anniv'])
    async def anniversaires(self, ctx):
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
            if len(dict_mois[i])==0:
                val = '```\n\n```'
            else:
                val = '```{0}```'.format('\n'.join([joueur.pseudo+' ('+str(joueur.anniv.day)+')' for joueur in dict_mois[i]]))
            embed.add_field(
                name=liste_mois[i-1],
                value=val,
                inline=True
            )
        await ctx.send(embed=embed)

    @commands.command(name='modifjoueur', aliases=['mj'])
    #async def modifjoueur(self, ctx, *args):
    async def modifjoueur(self, ctx, alias, attr, val):
        try:
            assert attr in ['statut', 'draps', 'prenom', 'pseudo', 'twitter', 'fc', 'anniv', 'num', 'exteams']
            i = alias_to_ind(alias)
            if len(i)>1:
                await ctx.send('Trop de joueurs correspondent à cet alias.', delete_after=10)
                return
            i = i[0] # ensures i is an int and not a list
            if attr in ['draps', 'exteams']:
                setattr(listejoueurs[i], attr, val.split(','))
            elif attr == 'anniv':
                setattr(
                    listejoueurs[i], 
                    attr, 
                    datetime.date(
                        year=int(val[4:8]), 
                        month=int(val[2:4]), 
                        day=int(val[0:2])
                    )
                )
            elif attr == 'statut':
                setattr(listejoueurs[i], attr, val.lower())
            else:
                setattr(listejoueurs[i], attr, val)
                if attr == 'pseudo':
                    listejoueurs[i].alias[0] = val

            with open(pickle_filename, 'wb') as f:
                pickle.dump(listejoueurs, f)

            await ctx.send('{0} de {1} modifié'.format(attr, listejoueurs[i].pseudo))
        except:
            await ctx.send('Usage incorrect', delete_after=30)

    @commands.command(name='fc')
    async def fc(self, ctx, *aliases):
        # syntax : $fc <j1> <j2> ...
        table = [['N°', 'Pseudo', 'FC']]
        if len(aliases)>=1:
            for i, joueur in enumerate(listejoueurs):
                if any(a.lower() in [alias.lower() for alias in aliases] for a in joueur.alias):
                    table.append([i, joueur.pseudo, 'SW-'+'-'.join([joueur.fc[0:4], joueur.fc[4:8], joueur.fc[8:12]])])
        elif len(aliases)==0:
            for i, joueur in enumerate(listejoueurs):
                table.append([i, joueur.pseudo, 'SW-'+'-'.join([joueur.fc[0:4], joueur.fc[4:8], joueur.fc[8:12]])])
        if len(table)==1:
            await ctx.send('Pseudo introuvable.')
            return
        output = tabulate(table, headers='firstrow', tablefmt='simple')
        await ctx.send('```{0}```'.format(output), delete_after=30)
            

    @commands.command(name='infosjoueurs', aliases=['ij'])
    async def infosjoueurs(self, ctx):
        # 943503741959700501
        assert ctx.author.id in adminlist

        # Delete all messages in channel
        await self.bot.get_channel(943503741959700501).purge()

        # Do the embed
        embed=discord.Embed(
            title="Liste des joueurs",  
            description="Bah c'est la liste des joueurs quoi", 
            color=0xFF5733,
            type='rich'
        )
        for j in listejoueurs[:24]:
            embed.add_field(name=j.affiche_title_embed(), value=j.affiche_value_embed(), inline=True)
        await self.bot.get_channel(943503741959700501).send(embed=embed)
        if len(listejoueurs)>24:
            embed=discord.Embed( 
            color=0xFF5733,
            type='rich'
            )
            for j in listejoueurs[24:]:
                embed.add_field(name=j.affiche_title_embed(), value=j.affiche_value_embed(), inline=True)
        
            await self.bot.get_channel(943503741959700501).send(embed=embed)

    @commands.command(name='tierlist', aliases=['tl'])
    async def tierlist(self, ctx):
        assert ctx.author.id in adminlist

        if not os.path.isdir('images'):
            os.mkdir('images')

        font_sizes = {1 : 50, 2 : 50, 3 : 55, 4 : 45, 5 : 36, 6 : 30, 7 : 26, 8 : 23, 9 : 20, 10 : 18, 11 : 16, 12 : 14}
        colors = {'m' : (0, 179, 255), 's' : (228, 180, 0)}
        font = 'RobotoMono-Regular.ttf'

        size = (128,128)
        bordersize = 4
        center = size[0]//2-25

        template_array = np.zeros(size)
        template_array[bordersize:-bordersize,bordersize:-bordersize] = 255

        template_im = Image.fromarray(template_array)

        template_im = template_im.convert('RGB')
    
        #delete all images before creating new ones
        for f in os.listdir('images'):
            os.remove('images/'+f)

        for joueur in listejoueurs:
            template_copy = copy(template_im)

            d = ImageDraw.Draw(template_copy)

            my_font = ImageFont.truetype(font, font_sizes[len(joueur.pseudo)])
            d.text((10, center), joueur.pseudo, fill=colors[joueur.statut.lower()], font = my_font)

            template_copy.save('images/' + joueur.pseudo + '.png')
    
        await ctx.send('TL générée :+1:')

    @commands.command(name='alias')
    async def alias(self, ctx, *args):
        if len(args)==0:
            table = [['N°', 'Pseudo', 'Alias']]
            for i, joueur in enumerate(listejoueurs):
                liste_temp = [i] 
                liste_temp += [joueur.pseudo, joueur.alias]
                table.append(liste_temp)
            output = tabulate(table, headers='firstrow', tablefmt='simple')
            await ctx.send('```{0}```'.format(output))
            return

        ind = alias_to_ind(args[0])
        for i in ind:
            output = 'Les alias de {0} sont : {1}'.format(listejoueurs[i].pseudo, ', '.join(listejoueurs[i].alias))
            await ctx.send(output, delete_after=20)
        if len(ind)==0:
            await ctx.send('Aucun joueur trouvé.', delete_after=10)

    @commands.command(name='alias+')
    async def aliasp(self, ctx, *args):
        # Syntaxe : $alias+ <id> <alias1> <alias2>...
        ind = alias_to_ind(args[0])
        if len(ind)>1:
            await ctx.send('Trop de joueurs correspondent à cet alias ({0}). Essayez un autre.'.format(args[0]), delete_after=20)
            return
        else: 
            ind = ind[0]
            joueur = listejoueurs[ind]
            for alias in args[1:]:
                if alias not in joueur.alias:
                    joueur.alias.append(alias)
            with open(pickle_filename, 'wb') as f:
                pickle.dump(listejoueurs, f)
            await ctx.send('Alias ajoutés.', delete_after=20)

def setup(bot):
    bot.add_cog(Joueurs(bot))