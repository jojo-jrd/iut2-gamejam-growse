# Auteur : Monster Turck

# STL
import time

from src.element import Element
from src.animate_element import AnimateElement
from src.inventaire import Inventaire
from src.image import Image
from src.cannabis import Cannabis
from src.rose import Rose

# PyGames
import pygame
from pygame.locals import *

class Joueur(AnimateElement):

    # -- Constructors --

    def __init__(self, position, inventaire = None, main_char = False, difficulte = 1):
        super().__init__('stay', position)

        # Attrs
        self._mort = False
        self._gagnee = False
        self._inventaire = inventaire
        self.__main_char = main_char
        self.__difficulte = difficulte
        self.__movesCount = 0

    # -- Getters --

    @property
    def inventaire(self):
        return self._inventaire


    # -- Setters --

    @inventaire.setter
    def inventaire(self, value):
        self._inventaire = value


    # -- Tests --

    def isDead(self):
        return self._mort

    def aGagnee(self):
        return self._gagnee


    # -- Fonctionnalités --

    def kill(self):
        self._mort = True

    def win(self):
        self._gagnee = True


    # -- Loadings --

    def loadSprites(self, name, run = False):
        for i in range(1,6):
            if self.__main_char:
                img = Image((0,0), 'src/images/Personnage/' + name + '/run/' + name + '-run-'+ str(i) + '.png')
                img.alignment = 'center'
                self.addSprite('run', img)

            try:
                if not self.__main_char:
                    img = Image((0,0), 'src/images/Personnage/' + name + '/attack/' + name + '-attack-'+ str(i) + '.png')
                    img.alignment = 'center'
                    self.addSprite('attack', img)
            except FileNotFoundError:
                pass
            except pygame.error:
                pass

            img = Image((0,0), 'src/images/Personnage/' + name + '/walk/' + name + '-walk-'+ str(i) + '.png')
            img.alignment = 'center'
            self.addSprite('walk', img)

        for i in range(1,6):
            # Il n'existe pas le même nombre de sprite pour les amis
            try:
                img = Image((0,0), 'src/images/Personnage/' + name + '/dead/' + name + '-dead-'+ str(i) + '.png')
                img.alignment = 'center'
                self.addSprite('dead', img)
            except FileNotFoundError:
                pass
            except pygame.error:
                pass

        self.addSprite('dead-end', img)


        for i in range(1,3):
            img = Image((0,0), 'src/images/Personnage/' + name + '/hit/' + name + '-hit-'+ str(i) + '.png')
            img.alignment = 'center'
            self.addSprite('hit', img)

            img = Image((0,0), 'src/images/Personnage/' + name + '/stay/' + name + '-stay-'+ str(i) + '.png')
            img.alignment = 'center'
            self.addSprite('stay', img)

        img = Image((0,0), 'src/images/Personnage/' + name + '/stay/' + name + '-stay-4.png')
        img.alignment = 'center'
        self.addSprite('stay', img)

        self.animate('stay', 'stay', 2, True)


    # -- Update --

    def action(self, terrain):
        position = terrain.joueur.position[0]

        if 359 < position and position < 759:
            terrain.openBoutique()
        else:
            terrain.closeBoutique()

    def actionTime(self, window, clock, terrain, parent_position = (0,0)):
        pressed = pygame.key.get_pressed()

        if clock['name'] == 'player.keys':
            # Selection
            if pressed[pygame.K_1]:
                self._inventaire.set_selectionnee("weed")
            elif pressed[pygame.K_2]:
                self._inventaire.set_selectionnee("water")
            elif pressed[pygame.K_3]:
                self._inventaire.set_selectionnee("teq")
            elif pressed[pygame.K_4]:
                self._inventaire.set_selectionnee("rose")
            elif pressed[pygame.K_5]:
                self._inventaire.set_selectionnee("engrais")

            # Utilisation
            if pressed[pygame.K_e]: # POSER
                if terrain.verifPlante(self.position): # Pas de plante à cette endroit
                    item = self.inventaire.get_selectionnee()

                    if item in ['weed','rose','teq'] and self.inventaire.get_valeur_objet(item) > 0:
                        self.inventaire.soustraire_contenu(item, 1)

                        if(self.__difficulte==1):
                            engrais = 2
                        elif self.__difficulte == 2:
                            engrais = 5
                        else:
                            engrais = 10

                        if item == "rose":
                            plante = Rose("Rose", 1,{ "engrais": engrais,"eau": 0 }, 200, (0, 768 - 189))
                            plante.position = self.position
                            terrain.addPlante(plante)
                            soundPlanter = pygame.mixer.Sound("src/musics/effect/engrais.mp3")
                            soundPlanter.play()
                        elif item == "weed":
                            plante = Cannabis("Cannabis", 1, { "engrais": engrais}, 4 - self.__difficulte, (0, 768 - 189))
                            plante.position = self.position
                            terrain.addPlante(plante)
                            soundPlanter = pygame.mixer.Sound("src/musics/effect/engrais.mp3")
                            soundPlanter.play()
                        else:
                            terrain.useTeq()
                    else:
                        soundEchec = pygame.mixer.Sound("src/musics/effect/wrong.wav")
                        soundEchec.set_volume(0.3)
                        soundEchec.play()

            elif(pressed[pygame.K_a]): # AMELIORATION
                if(terrain.haricot.estFinie()):
                    window.stopSound()
                    window.runSound("src/musics/musique/end.mp3")

                    window.current_mode = 'victoire'
                else:
                    planteActuelle = terrain.getPlantePosition(self.position)
                    if(planteActuelle!=None):
                        reussi = planteActuelle.monterNiveau(self.inventaire)
                        if reussi:
                            soundNiveau = pygame.mixer.Sound("src/musics/effect/level.mp3")
                            soundNiveau.play()
                        else:
                            soundEchec = pygame.mixer.Sound("src/musics/effect/wrong.wav")
                            soundEchec.set_volume(0.3)
                            soundEchec.play()

            elif pressed[pygame.K_r]: # REGENERATION DE LA ROSE

                planteActuelle = terrain.getPlantePosition(self.position)
                if(planteActuelle!=None and type(planteActuelle)==Rose):
                    reussi = planteActuelle.regenerer(self.inventaire)
                    if reussi:
                        soundNiveau = pygame.mixer.Sound("src/musics/effect/water.mp3")
                        soundNiveau.play()
                    else:
                        soundEchec = pygame.mixer.Sound("src/musics/effect/wrong.wav")
                        soundEchec.set_volume(0.3)
                        soundEchec.play()

            elif pressed[pygame.K_ESCAPE]:
                window.current_mode = 'echap'

            else:
                distance = 30

                if pressed[pygame.K_q] or pressed[pygame.K_d]:
                    x = (distance, 0)

                    if pressed[pygame.K_q]:
                        distance = -distance

                    # Player
                    if (distance < 0 and self.position[0] > -terrain.max_left + self.size[0]) or (distance > 0 and self.position[0] < terrain.max_left + 1024 - self.size[0]):
                        self.__movesCount += 1

                        if self.__movesCount > 10:
                            distance *= 1.75

                            if not self.hasAnimation('run'):

                                self.stopAnimation()
                                self.animate('run', 'run', .75, True)
                        elif not self.hasAnimation('walk'):
                            self.stopAnimation()
                            self.animate('walk', 'walk', .5, True)

                        self.moveTo((distance, 0), clock['resetTime'])

                        # Terrain
                        if distance < 0 and terrain.position[0] < terrain.max_left - 32 and self.position[0] < terrain.max_left + 1024/2:
                            terrain.moveTo((-distance, 0), clock['resetTime'], False)
                            #self.inventaire.moveTo((distance, 0), clock['resetTime'], False)

                            #for img in terrain.spritesChiffre[terrain.manche]:
                            #    img.moveTo((distance, 0), clock['resetTime'], False)

                        if distance > 0 and terrain.position[0] > -terrain.max_left + 32 and self.position[0] > -terrain.max_left + 1024/2:
                            terrain.moveTo((-distance, 0), clock['resetTime'], False)
                            #self.inventaire.moveTo((distance, 0), clock['resetTime'], False)

                            #for img in terrain.spritesChiffre[terrain.manche]:
                            #    img.moveTo((distance, 0), clock['resetTime'], False)

            if self.__main_char and not self.isMoving() and not self.hasAnimation('stay'):
                self.__movesCount = 0
                self.stopAnimation()
                self.animate('stay', 'stay', 1, True)

        super().update(window, parent_position)
