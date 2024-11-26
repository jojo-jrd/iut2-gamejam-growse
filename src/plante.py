"""
Auteur : Josserand Jordan
"""

from src.element import Element
from src.image import Image

class Plante(Element):

    # Besoins est de la forme {"eau" : 5 , ... }

    def __init__(self, nom, niveau,besoins,position):
        super().__init__("main",position);
        self._nom = nom
        self._niveau = niveau
        self._besoins = besoins

    # DESTRUCTEUR

    def __del__(self):
        self.current_mode = 'mort'

    # GETTERS

    def getNom(self):
        return self._nom

    def getNiveau(self):
        return self._niveau

    def getBesoins(self):
        return self._besoins

    def getSprites(self):
        return self.__spritesChiffre

    # SETTERS

    def setNom(self, nom):
        self._nom = nom

    def setNiveau(self, niveau):
        self._niveau = niveau

    def setBesoins(self, besoins):
        self._besoins = besoins
