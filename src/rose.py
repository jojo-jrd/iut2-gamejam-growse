"""
Auteur : Josserand Jordan
"""

from src.plante import Plante
from src.image import Image
class Rose(Plante):

    # -- Constructors --

    def __init__(self, nom, niveau, besoins, vie, position):
        super().__init__(nom,niveau,besoins,position)

        # Loadings
        self.loadBackground("src/images/Rose/Rose-"+str(niveau)+".png")

        self.__list_vies = [ 100, 90, 80, 70, 60, 50, 35, 20, 10, 0 ]
        for i in self.__list_vies:
            img = Image((self.size[0] / 2, 135), 'src/images/vie/vie-' + str(i) + '.png')
            img.alignment = 'middle'
            img.size = (56, -1)
            self.addSprite('vie-' + str(i), img)

        # Attrs
        self.__vie_max = vie
        self.__vie = vie
        self.vie = vie

    # -- Getters --

    @property
    def vie(self):
        return self.__vie


    # -- Setters --

    @vie.setter
    def vie(self, value):
        near = 100
        for i in self.__list_vies:
            percent = 100 * value / self.__vie_max
            if abs(percent - i) < abs(percent - near):
                near = i

        self.current_mode = 'vie-' + str(near)

        self.__vie = value

        if self.__vie < self.__vie_max:
            besoins = self.getBesoins()

            for b in besoins.keys():
                if(b=="eau"):
                    besoins[b] = int( 10 - (self.__vie_max - self.__vie) / 10 )


    # -- Tests --

    def isDead(self):
        return self.__vie <= 0


    # -- Fonctionnalités --

    def monterNiveau(self,inventaire):
        nb_engrais = inventaire.get_valeur_objet('engrais')
        if(self.getNiveau()<5):
            besoins = self.getBesoins()
            for b in besoins.keys():
                if(b=="engrais"):
                    if(besoins[b]<=nb_engrais):
                        self.setNiveau(self.getNiveau()+1)
                        self.loadBackground("src/images/Rose/Rose-"+str(self.getNiveau())+".png")
                        inventaire.soustraire_contenu("engrais",besoins[b])
                        besoins[b] = int(besoins[b]*1.60)
                        return True
                    else:
                        return False
        return False

    def regenerer(self,inventaire):
        nb_eau = inventaire.get_valeur_objet('water')

        besoins = self.getBesoins()
        for b in besoins.keys():
            if(b=="eau"):
                if(besoins[b] <= nb_eau and besoins[b] > 0):
                    augmentation = min(besoins[b], nb_eau)
                    self.__vie += 10 * augmentation
                    inventaire.soustraire_contenu("water", augmentation)
                    besoins[b] -= augmentation
                    return True
                else:
                    return False
        return False
