import discord
from discord.ext import commands
import pickle

from main import counter_table, counter_table_filename

class Tables(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def submit(self, ctx, size, adv, *, data):
        #basic parameter checks
        if ctx.guild.id != 371688231076626433:
            await ctx.send("You cannot use this command in this server!")
            return
            
        size = int(size)

        # Split each word in each line
        lines = [line.split() for line in data.split('\n')]

        total_JPP = 0
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
                total_JPP += int(line[ind_score])
            else:
                total_adv += int(line[ind_score])

            if '+' in line[ind_score]: # 
                line[ind_score] = str(sum([int(num) for num in line[ind_score].split('+')]))

        total = total_JPP + total_adv

        if len(lines) != 2*size:
            await ctx.send('Le tableau doit contenir {0} entrées.'.format(2*size))

        print(lines)

        base_url_lorenzi = "https://gb.hlorenzi.com/table.png?data="

        table_text = '#title JPP vs {0}\n'.format(adv)
        for i in range(2):
            if i==0: # JPP
                table_text += 'JPP\n'
            else: # not JPP
                table_text += '{0}\n'.format(adv)
            for j in range(size):
                table_text += '{0}\n'.format(' '.join(lines[i*size+j]))
            
        url_table_text = urllib.parse.quote(table_text)
        image_url = base_url_lorenzi + url_table_text

        # --------------- #
        #      EMBED      #
        # --------------- #
        

        e = discord.Embed(title="Table")
        e.set_image(url=image_url)
        content = "Please react to this message with \U00002611 within the next 30 seconds to confirm the table is correct"
        if total != normal_total[size]:
            warning = ("The total score of %d might be incorrect! Most tables should add up to %d points"
                       % (total, normal_total[size]))
            e.add_field(name="Warning", value=warning)
        embedded = await ctx.send(content=content, embed=e)

        #ballot box with check emoji
        CHECK_BOX = "\U00002611"
        X_MARK = "\U0000274C"
        await embedded.add_reaction(CHECK_BOX)
        await embedded.add_reaction(X_MARK)

        def check(reaction, user):
            if user != ctx.author:
                return False
            if reaction.message != embedded:
                return False
            if str(reaction.emoji) == X_MARK:
                return True
            if str(reaction.emoji) == CHECK_BOX:
                return True
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
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
            chan = self.bot.get_channel(930934616485949500)

            await embedded.delete()
            
            if total_JPP > total_adv: # WIN
                counter_table[0][0] += 1
                title = 'Win #{0} vs {1}'.format(counter_table[0][0], adv)
            elif total_JPP < total_adv: # LOSE
                counter_table[0][2] += 1
                title = 'Lose #{0} vs {1}'.format(counter_table[0][2], adv)
            else:                        # TIE
                counter_table[0][1] += 1
                title = 'Tie #{0} vs {1}'.format(counter_table[0][1], adv)

            e = discord.Embed(title=title)
            e.set_image(url=image_url)
            #content = "Please react to this message with \U00002611 within the next 30 seconds to confirm the table is correct"
            #if total != normal_total[size]:
             #   warning = ("The total score of %d might be incorrect! Most tables should add up to %d points"
              #         % (total, normal_total[size]))
               # e.add_field(name="Warning", value=warning)
            await chan.send(embed=e)


            return
    
    @commands.command()
    async def counter(self, ctx, *args):
        # counter 
        # counter friendly 0 0 0
        # counter offi 0 0 0

        if len(args)==0:
            await ctx.send('Le compteur est à : {0}'.format(counter_table))
            return
        
        war_type = args[0]
        win, tie, lose = int(args[1]), int(args[2]), int(args[3])

        if war_type == 'friendly': i=0
        elif war_type == 'offi': i=1
        counter_table[i] = [win, tie, lose]
        with open(counter_table_filename, 'wb') as f:
            pickle.dump(counter_table, f)
        await ctx.send('Compteur réglé à {0}'.format(counter_table[i]))

def setup(bot):
    bot.add_cog(Tables(bot))