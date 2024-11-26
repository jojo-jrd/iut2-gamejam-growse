"""
Auteur : Josserand Jordan
"""

from src.plante     import Plante
from src.inventaire import Inventaire
from src.image import Image

from random import randint
import time

class Cannabis(Plante):

    def __init__(self,nom,niveau,besoins,puissance,position):
        super().__init__(nom,niveau,besoins,position)
        self.__puissance = puissance
        self.loadBackground("src/images/Weed/weed-1.png")

    # GETTERS

    def getPuissance(self):
        return self.__puissance

    # SETTERS

    def setPuissance(self,puissance):
        self.__puissance = puissance

    # FONCTIONNALITES

    def monterNiveau(self,inventaire):
        nb_engrais = inventaire.get_valeur_objet('engrais')

        if(self.getNiveau()!=3):
            besoins = self.getBesoins()
            for b in besoins.keys():
                if(b=="engrais"):
                    if(besoins[b]<=nb_engrais):
                        self.setNiveau(self.getNiveau()+1)
                        if(self.getNiveau()<3):
                            self.loadBackground("src/images/Weed/weed-"+str(self.getNiveau())+".png")
                        else:
                            self.loadBackground("src/images/Weed/weed-3.png")

                        inventaire.soustraire_contenu("engrais",besoins[b])
                        return True
                    else:
                        return False
        return False
