"""
Auteur : Josserand Jordan
"""

from src.element import Element

class Objet(Element):
    def __init__(self,nom,prix,position):
        super().__init__("main",position);
        self.__nom = nom
        self.__prix = prix

    # DESTRUCTEUR

    def __del__(self):
        self.current_mode = 'mort'

    # GETTERS

    def getNom(self):
        return self.__nom

    def getPrix(self):
        return self.__prix

    # SETTERS

    def setNom(self,nom):
        self.__nom = nom

    def setPrix(self,prix):
        self.__prix = prix
