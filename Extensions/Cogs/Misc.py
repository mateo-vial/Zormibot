import discord
from discord.ext import commands
import random
import os
from tabulate import tabulate

from main import adminlist, chancmdlist, toggles

def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 135495101496426496
    return commands.check(predicate)

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send('Hello world!')

    @commands.command(name='miaule')
    async def miaule(self, ctx):
        await ctx.send('Miaou :cat:')

    @commands.command(name='stoptwitter')
    async def stoptwitter(self, ctx, *args):
        await ctx.send('Bot twitter `@bFlo17` désactivé.', delete_after=20)

    @commands.command(name='teps')
    async def teps(self, ctx):
        await ctx.send(
            file = discord.File(random.choice(['Assets/prout/{0}'.format(file) for file in os.listdir('prout')])), 
            delete_after = 10
        )
    
    @is_me()
    @commands.command(name='stop')
    async def stop(self, ctx):
        try:
            await ctx.send('Ciao.')
        except: 
            print('permission message manquant')
        exit()

    @commands.command()
    @commands.has_role('Enfants')
    async def bb(self, ctx):
        await ctx.send('Tu es un enfant :+1:')

    @commands.command()
    async def startwar(self, ctx, home, away):
        await ctx.send('War commencé entre {0} et {1}'.format(home, away))

        total_home = 0
        total_away = 0
        total_diff = 0

        list_tabulate = [['Course', home, 'Diff', away]]

        scores = {
            12: 1, 11: 2, 10: 3, 9: 4, 8: 5, 7: 6, 
            6: 7, 5: 8, 4: 9, 3: 10, 2: 12, 1: 15
        }
        def fun_score(x): return scores[x]

        count = 0

        def check(msg):
            return msg.author == ctx.author and (all(c in '0123456789 ' for c in msg.content) or msg.content == 'stop')

        while count < 12:
            await ctx.send('Entre les spots de la course N°{0} séparés par des espaces. `stop` pour abandonner.'.format(count+1))
            msg = await self.bot.wait_for('message', check=check)

            if msg.content.lower() == 'stop':
                await ctx.send('War abandonné.')
                return

            spots = list(map(int, msg.content.split()))

            if all(((spot in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] for spot in spots),
                    len(spots) == 6,
                    len(spots) == len(set(spots))
            )):
                count += 1

                course_home = sum(map(fun_score, spots))
                course_away = 82 - course_home
                course_diff = 2*course_home - 82

                total_home += course_home
                total_away += course_away
                total_diff += course_diff

                list_tabulate.append([count, course_home, '{0:+}'.format(course_diff), course_away])
                await ctx.send('```{0}```'.format(
                    tabulate(list_tabulate + [
                        ['---','---','---','---'],
                        ['TOTAL', total_home, '{0:+}'.format(total_diff), total_away]
                    ])  
                ))
            else:
                await ctx.send('Spots incorrects.')

        await ctx.send('War terminé.')
        return

    @is_me()
    @commands.command(name='toggle')
    async def toggle(self, ctx, fonctionnalite=None):
        if fonctionnalite in toggles:
            toggles[fonctionnalite] = not toggles[fonctionnalite]
            if toggles[fonctionnalite]:
                mot = 'activé'
            else:
                mot = 'désactivé'
            await ctx.send('{0} {1}'.format(fonctionnalite, mot), delete_after=20)
            return 

        if fonctionnalite == None:
            table = [['Fonctionnalité', 'État']]
            for fonc in toggles:
                table.append([fonc, toggles[fonc]])
            output = tabulate(table, headers='firstrow', tablefmt='simple')
            await ctx.send('```{0}```'.format(output), delete_after=20)
            return

        await ctx.send('fonctionnalité erronée.', delete_after=10)
        return

    @commands.command(name='version')
    async def version(self, ctx):
        await ctx.send(discord.__version__, delete_after=20)
        
        
def setup(bot):
    bot.add_cog(Misc(bot))