import discord
from discord.ext import commands
import pickle
import urllib
import os

from main import counter_table, counter_table_filename, adminlist

class Tables(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role('JPP')
    @commands.command()
    async def submit(self, ctx, mode, size:int, home, adv, *, data):
        #basic parameter checks
        if ctx.guild.id != 371688231076626433:
            await ctx.send("You cannot use this command in this server!")
            return
        if mode not in ['offi', 'friendly', 'intra']:
            await ctx.send('Mode incorrect.')
            return
        if size not in [1, 2, 3, 4, 5, 6]:
            await ctx.send('Size incorrect.')
            return

        # Wait for message for style argument
        await ctx.send('Style (default/dark/mku) ? (5s)')
        
        def check1(m):
            return (m.content in ['mku', 'dark', 'default']) and (m.author == ctx.author)

        try:
            msg = await self.bot.wait_for('message', timeout=5.0, check=check1)
            style = msg.content
        except:
            await ctx.send('style default car tu es long.')
            style = 'default'
        
        # Split each word in each line
        lines = [line.split() for line in data.split('\n')]

        total_home = 0
        total_adv = 0
        normal_total = [0, 48, 132, 288, 468, 696, 984]

        # Fix lines (add brackets to flag and sum up if there is a +)
        for i, line in enumerate(lines):

            if len(line)==3: # if there is a flag
                line[1] = '[{0}]'.format(line[1]) # add brackets
                ind_score = 2 # the score will be in index 2
            else:
                ind_score = 1 # the score is in index 1
            
            if i<size:
                total_home += int(line[ind_score])
            else:
                total_adv += int(line[ind_score])

            if '+' in line[ind_score]: # 
                line[ind_score] = str(sum([int(num) for num in line[ind_score].split('+')]))

        total = total_home + total_adv

        if len(lines) != 2*size:
            await ctx.send('Le tableau doit contenir {0} entrées.'.format(2*size))

        base_url_lorenzi = "https://gb.hlorenzi.com/table.png?data="

        table_text = '#title {0} vs {1}\n#style {2}\n'.format(home, adv, style)
        for i in range(2):
            if i==0: # JPP
                table_text += '{0}\n'.format(home)
            else: # not JPP
                table_text += '{0}\n'.format(adv)
            for j in range(size):
                table_text += '{0}\n'.format(' '.join(lines[i*size+j]))
        print(table_text)
        url_table_text = urllib.parse.quote(table_text)
        image_url = base_url_lorenzi + url_table_text
        

        e = discord.Embed(title="Table")
        e.set_image(url=image_url)
        content = "Réagissez avec \U00002611 dans les 30 secondes pour confirmer"
        if total != normal_total[size]:
            warning = ("Le score total  (%d) est peut être incorrect ! Le tableau devrait avoir un total de %d points"
                       % (total, normal_total[size]))
            e.add_field(name="Warning", value=warning)
        embedded = await ctx.send(content=content, embed=e)

        #ballot box with check emoji
        CHECK_BOX = "\U00002611"
        X_MARK = "\U0000274C"
        await embedded.add_reaction(CHECK_BOX)
        await embedded.add_reaction(X_MARK)

        def check2(reaction, user):
            if user != ctx.author:
                return False
            if reaction.message != embedded:
                return False
            if str(reaction.emoji) == X_MARK:
                return True
            if str(reaction.emoji) == CHECK_BOX:
                return True
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check2)
        except:
            await embedded.delete()
            return

        if str(reaction.emoji) == X_MARK:
            await embedded.delete()
            return
        if str(reaction.emoji) == CHECK_BOX:
            # 930934616485949500 infos joueurs test
            # 815641948776955905 résultats
            # 815647761528520715 résultats offis
            # chan = self.bot.get_channel(930934616485949500)

            await embedded.delete()
            
            # Increment counter and generate title name
            if mode == 'intra':
                counter_table[2] += 1
                count_temp = counter_table[2]
                title = 'Intra #{0}'.format(counter_table[2])
                path_ = ''
                chan = self.bot.get_channel(815641948776955905)
            else:
                if mode == 'friendly': 
                    ind_incr = 0
                    chan = self.bot.get_channel(815641948776955905)
                elif mode == 'offi': 
                    ind_incr = 1
                    chan = self.bot.get_channel(815647761528520715)

                if total_home > total_adv: # WIN
                    counter_table[ind_incr][0] += 1
                    count_temp = counter_table[ind_incr][0]
                    title = 'Win #{0} vs {1}'.format(counter_table[ind_incr][0], adv)
                    path_ = 'win/'
                elif total_home < total_adv: # LOSE
                    counter_table[ind_incr][2] += 1
                    count_temp = counter_table[ind_incr][2]
                    title = 'Lose #{0} vs {1}'.format(counter_table[ind_incr][2], adv)
                    path_ = 'lose/'
                else:                        # TIE
                    counter_table[ind_incr][1] += 1
                    count_temp = counter_table[ind_incr][1]
                    title = 'Tie #{0} vs {1}'.format(counter_table[ind_incr][1], adv)
                    path_ = 'tie/'

            # save the counter after incrementing it
            with open(counter_table_filename, 'wb') as f:
                pickle.dump(counter_table, f)

            # embed
            e = discord.Embed(title=title)
            e.set_image(url=image_url)
            await chan.send(embed=e)

            # save image locally
            if True:
                urllib.request.urlretrieve(image_url, 'Tables/{0}/{1}{2}.jpg'.format(mode, path_, count_temp))


            return
    
    @commands.has_role('JPP')
    @commands.command()
    async def counter(self, ctx, *args):
        # counter 
        # counter intra 0
        # counter friendly 0 0 0
        # counter offi 0 0 0

        if len(args) == 0:
            await ctx.send('Le compteur est à : {0}'.format(counter_table))
            return
        
        elif len(args) == 2:
            assert args[0] == 'intra'
            war_type = args[0]
            val = int(args[1])
            counter_table[2] = val
            with open(counter_table_filename, 'wb') as f:
                pickle.dump(counter_table, f)
            await ctx.send('Compteur réglé à {0}'.format(counter_table[2]))
            return
        
        elif len(args) == 4:
            war_type = args[0]
            win, tie, lose = int(args[1]), int(args[2]), int(args[3])

        if war_type == 'friendly': i=0
        elif war_type == 'offi': i=1
        counter_table[i] = [win, tie, lose]
        with open(counter_table_filename, 'wb') as f:
            pickle.dump(counter_table, f)
        await ctx.send('Compteur réglé à {0}'.format(counter_table[i]))

    @commands.has_role('JPP')
    @commands.command()
    async def cleartables(self, ctx):
        assert ctx.author.id in adminlist
        # clears all table images in local folders
        for root, dirs, files in os.walk('Tables/'):
            for file in files:
                os.remove('{0}/{1}'.format(root,file))
        await ctx.send('Images supprimées :+1:', delete_after=10)

def setup(bot):
    bot.add_cog(Tables(bot))