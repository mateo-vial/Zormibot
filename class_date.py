class Date:
    def __init__(self, annee, mois, jour):
        self.annee = annee
        self.mois = mois
        self.jour = jour

    def bissextile(self):
        return (self.annee % 4 == 0 and self.annee % 100 != 0) or (self.annee % 400 == 0)

    def njour(self):
        if not self.bissextile():
            mois_taille = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        else:
            mois_taille = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
        return mois_taille[self.mois-1] + self.jour
    