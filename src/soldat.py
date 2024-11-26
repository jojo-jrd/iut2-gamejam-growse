# Auteur : Monster Turck

import random
import time

from src.joueur import Joueur
from src.inventaire import Inventaire
from src.image import Image

class Soldat(Joueur):

    # -- Constructors --

    def __init__(self, player, isAmi, vie, attaque, position, inventaire, direction):
        if not isAmi:
            super().__init__(position, inventaire)
        else:
            super().__init__(position)
        # Attrs
        self._player = player
        self._isAmi = isAmi
        self._vie = vie
        self._force = attaque
        self._isLibre = True

        if not isAmi:
            self._inventaire.add_contenu("piece",5)
            self._inventaire.add_contenu("water",2 if random.randint(1,2) == 2 else 0)
            self._inventaire.add_contenu("teq", 1 if random.randint(1,20) == 20 else 0)
            self._inventaire.add_contenu("engrais",1 if random.randint(1,2) == 2 else 0)

        # Elements
        self.alignment = 'bottom-' + direction

        if not isAmi:
            self.loadSprites('enemy')
        else:
            self.loadSprites('ami')

        self.direction = direction
        self.size = (-1, 128)

        # Time
        self.startClock('combat', 1, False)
        self.startClock('dead', 1, False)


    # -- Getters --

    @property
    def player(self):
        return self._player

    @property
    def vie(self):
        return self._vie

    @property
    def force(self):
        return self._force


    # -- Setters --

    @player.setter
    def player(self, value):
        self._player = value

    @vie.setter
    def vie(self, value):
        self._vie = value

        if value <= 0:
            self._isLibre = False
            self.animate('dead', 'dead', 1)
            self.restartClock('dead')

    @force.setter
    def force(self, value):
        self._force = value


    # -- Tests --

    def isAmi(self):
        return self._isAmi

    def isLibre(self):
        return self._isLibre


    # -- Fonctionnalités --

    def attaque(self, element):
        if self.isLibre():
            element.vie -= random.randint(max(self._force - 5, 0), self._force + 5)

            self.stopMove()
            self._isLibre = False
            self.animate('attack', 'attack', 1)
            self.restartClock('combat')

    def combat(self, soldat):
        self.attaque(soldat)

        if not soldat.isDead():
            soldat.attaque(self)

    def avance(self):
        if not self.isMoving() and not self._mort:
            if self.direction == 'left':
                self.moveTo((-30, 0), 1)
            else:
                self.moveTo(( 30, 0), 1)

            self.animate('walk', 'walk', 1, True)

    # -- Update --

    def updateTime(self, window, clock, parent_position = (0,0)):
        if clock['name'] == 'combat':
            self._isLibre = True
            self.avance()
        elif clock['name'] == 'dead':
            if self.vie <= 0:
                self._isLibre = True
                self.kill()
