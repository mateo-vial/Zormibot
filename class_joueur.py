class Joueur():
    def __init__(self, draps, pseudo, prenom, twitter, fc, anniv, num, exteams):
        """
        Je pars du principe que les champs draps, prenom, fc et anniv sont forcément renseignés
        """
        self.draps = draps # list of strings

        if pseudo != '/': self.pseudo = pseudo
        else: self.pseudo = None

        self.prenom = prenom # string

        if twitter != '/': self.twitter = twitter # string
        else: self.twitter = None

        self.fc = fc # string of numbers

        self.anniv = anniv # object Date

        if num != '/': self.num = num
        else: self.num = None

        if exteams != ['/']: self.exteams = exteams
        else: self.exteams = ['Aucune']

    def affiche(self):
        """
        Renvoie le string correspondant à l'affiche complète du joueur
        """
        output = ''

        # écriture des drapeaux
        output += ' '.join([':flag_{0}:'.format(drap) for drap in self.draps]) + ' '
        
        # écriture pseudo et prénom
        if self.pseudo != None:
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
            output += 'Anniversaire : ' + sep.join([str(self.anniv.jour).zfill(2), str(self.anniv.mois).zfill(2), str(self.anniv.annee)])
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

    def liste_affiche(self):
        # ['N°', 'Drapeaux', 'Pseudo', 'Prénom', 'Twitter', 'FC', 'Anniv', 'Num', 'Ex-teams']

        try:
            at_twitter = '@'+self.twitter
        except:
            at_twitter = None

        return [
            ', '.join(self.draps), 
            self.pseudo, 
            self.prenom, 
            at_twitter, 
            'SW-'+'-'.join([
                self.fc[0:4],
                self.fc[4:8],
                self.fc[8:12]
            ]), 
            '/'.join([str(self.anniv.jour).zfill(2), str(self.anniv.mois).zfill(2), str(self.anniv.annee)]),
            self.num,
            ', '.join(self.exteams)
        ]

    

        


