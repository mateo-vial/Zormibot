class Joueur():
    def __init__(self, statut, draps, pseudo, prenom, twitter, fc, anniv, num, exteams, id_discord):
        """
        Je pars du principe que les champs draps, prenom, fc et anniv sont forcément renseignés
        """
        self.statut = statut.lower() # 'm' ou 's' pour membre/stagiaire ou 'r' pour retraité

        self.draps = draps # list of strings

        if pseudo != '/': 
            self.pseudo = pseudo
        else: 
            self.pseudo = prenom

        # Alias
        self.alias = [self.pseudo] #list of strings

        self.prenom = prenom # string

        if twitter != '/': self.twitter = twitter # string
        else: self.twitter = None

        self.fc = fc # string of numbers

        self.anniv = anniv # object datetime.date

        if num != '/': self.num = num
        else: self.num = None

        if exteams != ['/']: self.exteams = exteams
        else: self.exteams = ['Aucune']

        if id_discord != '/': self.id_discord = int(id_discord)
        else: self.id_discord = None

    def affiche(self):
        """
        Renvoie le string correspondant à l'affiche complète du joueur
        """
        output = ''

        emojidict = {'m' : ':blue_circle:', 's' : ':yellow_circle:'}
        output += emojidict[self.statut.lower()] + '  '

        # écriture des drapeaux
        output += ' '.join([':flag_{0}:'.format(drap) for drap in self.draps]) + ' '
        
        # écriture pseudo et prénom
        if self.pseudo != self.prenom:
            output += self.pseudo+'/'
        output += self.prenom

        # écriture twitter
        if self.twitter != None:
            output += ', Twitter : ``@{0}``'.format(self.twitter)

        output += '\n```'

        # écriture FC
        if self.fc != None:
            prefix_fc = 'SW-'
            sep = '-'
            # output += 'FC : '+ prefix + self.fc[0:4] + sep + self.fc[4:8] + sep + self.fc[8:12]
            output += 'FC : ' + prefix_fc + sep.join([self.fc[0:4], self.fc[4:8], self.fc[8:12]])
            output += '\n' 

        # écriture Anniv
        if self.anniv != None:
            sep = '/'
            output += 'Anniversaire : ' + sep.join([str(self.anniv.day).zfill(2), str(self.anniv.month).zfill(2), str(self.anniv.year)])
            output += '\n'

        # écriture Num
        if self.num != None:
            sep = ' '
            output += 'Num : '
            if len(self.num) == 10:
                output += sep.join([self.num[0:2], self.num[2:4], self.num[4:6], self.num[6:8], self.num[8:10]])
            else:
                output += self.num
            output += '\n'

        # écriture Ex-team
        sep = ', '
        output += 'Ex-team MK8D : '
        output += sep.join(self.exteams)

        # fin
        output += '```'
        return output

    def affiche_title_embed(self):
        output = ''

        # Symbole stagiaire/membre
        emojidict = {
            'm' : ':blue_circle:', 
            's' : ':yellow_circle:', 
            'r': ':orange_circle:'
        }
        output += emojidict[self.statut.lower()] + '  ' #espace insecable

        # drapeaux
        output += ' '.join([':flag_{0}:'.format(drap) for drap in self.draps]) + ' ' #espace insecable

        # pseudo/prenom
        if self.pseudo != self.prenom:
            output += self.pseudo+'/'
        output += self.prenom

        return output

    def affiche_value_embed(self):
        output = ''

        #   écriture twitter
        if self.twitter != None:
            output += 'Twitter : ``@{0}``\n'.format(self.twitter) #espace insecable
        
        output += '```'
        # écriture FC
        if self.fc != None: # en principe c jamais none...
            prefix_fc = 'SW-'
            sep = '-'
            # output += 'FC : '+ prefix + self.fc[0:4] + sep + self.fc[4:8] + sep + self.fc[8:12]
            output += 'FC : ' + prefix_fc + sep.join([self.fc[0:4], self.fc[4:8], self.fc[8:12]]) + '\n' #insecable

        # écriture anniv
        if self.anniv != None:
            sep = '/'
            output += 'Anniversaire : ' + sep.join([str(self.anniv.day).zfill(2), str(self.anniv.month).zfill(2), str(self.anniv.year)])
            output += '\n' #insecable

        # écriture num
        if self.num != None:
            sep = ' '
            output += 'Num : '#insecable
            if len(self.num) == 10:
                output += sep.join([self.num[0:2], self.num[2:4], self.num[4:6], self.num[6:8], self.num[8:10]])
            else:
                output += self.num
            output += '\n'
        
        # écriture Ex-team
        sep = ', '
        output += 'Ex-team MK8D : ' #insecable
        output += sep.join(self.exteams)

        output += '```'
    
        return output

    def liste_affiche(self):
        # ['N°', 'Statut', 'Drapeaux', 'Pseudo', 'Prénom', 'Twitter', 'FC', 'Anniv', 'Num', 'Ex-teams']

        try:
            at_twitter = '@'+self.twitter
        except:
            at_twitter = None
        
        if self.pseudo != self.prenom:
            pseud_temp = self.pseudo
        else:
            pseud_temp = None

        return [
            self.statut.upper(),
            ','.join(self.draps), 
            pseud_temp, 
            self.prenom, 
            at_twitter, 
            'SW-'+'-'.join([
                self.fc[0:4],
                self.fc[4:8],
                self.fc[8:12]
            ]), 
            '/'.join([str(self.anniv.day).zfill(2), str(self.anniv.month).zfill(2), str(self.anniv.year)]),
            self.num,
            ','.join(self.exteams),
        ]

    

        


