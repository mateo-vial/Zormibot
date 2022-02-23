import discord
from discord.ext import commands
import re
import io
import json
import urllib
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

        # only 6V6
        #size=6
        size = int(size)

        #functions for parsing lorenzi table data
        def isGps(scores:str):
            gps = re.split("[|+]", scores)
            for gp in gps:
                if gp.strip().isdigit() == False:
                    return False
        def sumGps(scores:str):
            gps = re.split("[|+]", scores)
            sum = 0
            for gp in gps:
                sum += int(gp.strip())
            return sum
        def removeExtra(line):
            splitLine = line.split()
            if line.strip() == "":
                return False
            if len(splitLine) == 1:
                return False
            scores = splitLine[len(splitLine)-1]
            if scores.isdigit() == False and isGps(scores) == False:
                return False
            else:
                return True

        lines = filter(removeExtra, data.split("\n"))
        names = []
        scores = []
        for line in lines:
            # removes country flag brackets
            newline = re.sub("[\[].*?[\]]", "", line).split()
            names.append(" ".join(newline[0:len(newline)-1]))
            gps = newline[len(newline)-1]
            scores.append(sumGps(gps))
        if len(names) != 2*size:
            await ctx.send("Your table does not contain {0} valid score lines, try again!".format(2*size))
            return

        """
        #checking names with the leaderboard API
        nameAPIchecks = await API.get.checkNames(names)
        err_str = ""
        for i in range(12):
            if nameAPIchecks[i] is False:
                if len(err_str) == 0:
                    err_str += "The following players cannot be found on the leaderboard:\n"
                err_str += "%s\n" % names[i]
        if len(err_str) > 0:
            await ctx.send(err_str)
            return
        """
            
        total = sum(scores)
        normal_total = [0, 48, 132, 288, 468, 696, 984]
        teamscores = []
        teamnames = []
        teamplayerscores = []
        for i in range(2):
            teamscore = 0
            tnames = []
            pscores = []
            for j in range(size):
                teamscore += scores[i*size+j]
                #tnames.append(nameAPIchecks[i*size+j])
                tnames.append(names[i*size+j])
                pscores.append(scores[i*size+j])
            teamscores.append(teamscore)
            teamnames.append(tnames)
            teamplayerscores.append(pscores)

        sortedScoresTeams = sorted(zip(teamscores, teamnames, teamplayerscores), reverse=True)
        sortedScores = [x for x, _, _ in sortedScoresTeams]
        sortedTeams = [x for _, x, _ in sortedScoresTeams]
        sortedpScores = [x for _, _, x in sortedScoresTeams]
        sortedNames = []
        tableScores = []
        placements = []
        for i in range(len(sortedScores)):
            sortedNames += sortedTeams[i]
            tableScores += sortedpScores[i]
            if i == 0:
                placements.append(1)
                continue
            if sortedScores[i] == sortedScores[i-1]:
                placements.append(placements[i-1])
                continue
            placements.append(i+1)

        base_url_lorenzi = "https://gb.hlorenzi.com/table.png?data="
        if size > 1:
            table_text = ("#title JPP vs %s\n"
                          % (adv))
        print('placements : ', placements)
        print('sorted teams : ',sortedTeams)
        print('sortedpscores : ', sortedpScores)
        for i in range(int(12/size)):
            if size != 1:
                if i % 2 == 0:
                    teamcolor = "#1D6ADE"
                else:
                    teamcolor = "#4A82D0"
                table_text += "%d %s\n" % (placements[i], teamcolor)
            for j in range(size):
                index = size * i + j
                table_text += ("%s %d\n"
                               % (sortedTeams[i][j], sortedpScores[i][j]))
    
        url_table_text = urllib.parse.quote(table_text)
        image_url = base_url_lorenzi + url_table_text
    

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
        '''

        success, sentTable = await API.post.createTable(tier.upper(), sortedTeams, sortedpScores, ctx.author.id)
        if success is False:
            await ctx.send("An error occurred trying to send the table to the website!\n%s"
                           % sentTable)
            return
        newid = sentTable["id"]
        tableurl = ctx.bot.site_creds["website_url"] + sentTable["url"]

        e = discord.Embed(title="Mogi Table", colour=int("0A2D61", 16))

        e.add_field(name="ID", value=newid)
        e.add_field(name="Tier", value=tier.upper())
        e.add_field(name="Submitted by", value=ctx.author.mention)
        e.add_field(name="View on website", value=(ctx.bot.site_creds["website_url"] + "/TableDetails/%d" % newid))

        e.set_image(url=tableurl)
        channel = ctx.guild.get_channel(channels[tier.upper()])

        tableMsg = await channel.send(embed=e)
        
        await API.post.setTableMessageId(newid, tableMsg.id)
        await embedded.delete()
        if channel == ctx.channel:
            await ctx.message.delete()
        else:
            await ctx.send("Successfully sent table to %s `(ID: %d)`" %
                           (channel.mention, newid))
        '''

    @commands.command()
    async def submit2(self, ctx, size, adv, *, data):
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