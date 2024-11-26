# Auteur : Beaufils Tao

# STL
import time

from src.element    import Element
from src.inventaire import Inventaire
from src.text       import Text
from src.button     import Button

# PyGames
import pygame
from pygame.locals import *

class Boutique(Inventaire):

    # -- Constructors --

    def __init__(self, selectionnee, position):
        super().__init__(666, selectionnee, position)

        self.current_mode = 'main'

        # Setup
        self._contenu['weed'] = 20
        self._contenu['water'] = 10
        self._contenu['rose'] = 20
        self._contenu['engrais'] = 15

        self.__transaction = False

    def initSprites(self):
        self._list.remove('piece')
        self._list.remove('teq')

        self.loadBackground('src/images/Shop/shop-fr.png', (-1, 256), 'fr')
        self.loadBackground('src/images/Shop/shop-en.png', (-1, 256), 'en')

        i = 0
        for item in self._list:
            button = Button((int(i/2) * 120 + 75, (i%2) * 75 + 110), self.createTransaction)
            button.loadBackground('src/images/Shop/acheter-1.png', (-1, 32), 'fr')
            button.loadBackground('src/images/Shop/buy-1.png', (-1, 32), 'en')
            button.alignment = 'middle'

            self.addSprite('main', button)
            i += 1

    # -- Fonctionnalités --

    def createTransaction(self, window, position):
        self.__transaction = True

        if position[0] >= 157:
            # Cannabis ou seau d'eau
            if position[1] >= 153:
                # Seau d'eau
                self._selectionnee = 'water'
            else:
                # Cannabis
                self._selectionnee = 'weed'
        else:
            # Rose ou sac d'engrais
            if position[1] >= 153:
                # Sac d'engrais
                self._selectionnee = 'engrais'
            else:
                # Rose
                self._selectionnee = 'rose'


    def acheter(self, terrain):
        self.__transaction = False
        sous = terrain.joueur.inventaire.get_valeur_objet('piece')

        if sous >= self._contenu[self._selectionnee]:
            terrain.joueur.inventaire.add_contenu(self._selectionnee, 1)
            terrain.joueur.inventaire.soustraire_contenu('piece', self._contenu[self._selectionnee])

    # -- Update --

    def action(self, terrain):
        if self.__transaction:
            self.acheter(terrain)
