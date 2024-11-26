"""
Auteur : Josserand Jordan
"""

import time
from random import randint

from src.element import Element
from src.cannabis import Cannabis
from src.animate_element import AnimateElement
from src.image import Image
from src.joueur import Joueur
from src.inventaire import Inventaire
from src.haricot import Haricot
from src.rose import Rose
from src.soldat import Soldat
from src.text import Text
from src.cannabis import Cannabis
from src.boutique import Boutique

# PyGames
import pygame
from pygame.locals import *

class Terrain(AnimateElement):

    # -- Constructors --

    def __init__(self, position = (0,0)):
        super().__init__('main', position);

    def initialisation(self, window, manche, difficulte, position = (0,0)):
        self.removeMode('main')

        self.__manche = manche
        self.__difficulte = difficulte

        self.__isNight = False

        self.__inventaire = Inventaire(1000, "weed", (1024/2,700))
        self.__inventaire.add_contenu('piece', 120)

        self.__plantes = []
        self.__soldats = { "amis": [], "enemies": [] }

        self.__boutiqueOuverte = False
        self.__boutique = Boutique('weed', (( 759 - 359 ) / 2 + 359, 768 / 2 - 100))
        self.__boutique.alignment = 'bottom-center'

        # Time
        self.startClock('manche', max(30 - 0.1 * manche, 1), False)
        self.startClock('cannabis', 45)
        self.startClock('player.keys' , .125) # Vitesse d'appuie du joueur
        self.startClock('player.moves' , .4) # Vitesse d'appuie du joueur


        self.__ami_generation = []
        self.__enemy_generation = []

        self.startClock('ami.generation', 3)
        self.startClock('enemy.generation', 1.5)

        # Elements
        self.__background = AnimateElement('day')
        self.__max_left = 0

        # Jour
        img = Image((0,0), 'src/images/Map/day.png'  , (-1, 768))
        self.__max_left = (img.size[0] - 1024) / 2
        img.position = (-(img.size[0] - 1024) / 2, 0)
        img.alignment = 'top-left'
        self.__background.addSprite('day', img)

        # Transition 1
        for i in range(1,2):
            img = Image((0,0), 'src/images/Map/day-' + str(i) + '.png'  , (-1, 768))
            img.position = (-(img.size[0] - 1024) / 2, 0)
            img.alignment = 'top-left'
            self.__background.addSprite('transition.day', img)

        # Nuit
        img = Image((0,0), 'src/images/Map/night.png'  , (-1, 768))
        img.position = (-(img.size[0] - 1024) / 2, 0)
        img.alignment = 'top-left'
        self.__background.addSprite('night', img)

        # Transition 1
        for i in range(1,3):
            img = Image((0,0), 'src/images/Map/night-' + str(i) + '.png'  , (-1, 768))
            img.position = (-(img.size[0] - 1024) / 2, 0)
            img.alignment = 'top-left'
            self.__background.addSprite('transition.night', img)

        # Animation
        self.startClock('transition.day', 3, False, True)
        self.startClock('transition.night', 4, False, True)
        #self.__background.animate('day', 'night', max(30 - 0.1 * self.__manche, 1))


        self.__joueur = Joueur((1024 / 2, 768 - 179),self.__inventaire,True,self.__difficulte)
        self.__joueur.alignment = 'bottom-center'
        self.__joueur.loadSprites('mate')
        self.__joueur.size = (-1, 128)

        self.__emplacementDispo = []
        self.__emplacementTotal = []

        pos = -(self.__max_left) + 2 * self.__joueur.size[0]
        stop = (self.__max_left)+1024 - 2 * self.__joueur.size[0]
        while pos < stop:
            if not ( 359 <= pos and pos <= 759 ):
                self.__emplacementDispo.append(pos)
                self.__emplacementTotal.append(pos)
            pos += 100

        # Haricot

        self.__haricot  = Haricot ("Haricot" , 1, { "engrais": 2         },      (self.__emplacementDispo[14], 768 - 179))


        # Adds
        self.spritesChiffre = {}

        self.addSprite('main', self.__background)
        self.addSprite('main', self.__joueur)

        self.addPlante(self.__haricot)
        window.addSprite('jeu',self.__inventaire)
        self.loadSpriteManche(window)


        self.__round = Text((970,3),"Round : ","src/fonts/Minecraft.ttf",25)
        self.__round.alignment = "top-right"
        self.__round.setup_chiffre(self.__manche)


    # -- Getters --

    @property
    def manche(self):
        return self.__manche

    @property
    def joueur(self):
        return self.__joueur

    @property
    def plantes(self):
        return self.__plantes

    @property
    def soldats(self):
        return self.__soldats

    @property
    def amis(self):
        return self.__soldats["amis"]

    @property
    def enemies(self):
        return self.__soldats["enemies"]

    @property
    def difficulte(self):
        return self.__difficulte

    @property
    def max_left(self):
        return self.__max_left

    @property
    def haricot(self):
        return self.__haricot

    # -- Setters --

    @manche.setter
    def manche(self, value):
        self.__manche = value

    @difficulte.setter
    def difficulte(self, value):
        self.__difficulte = value

    @haricot.setter
    def haricot(self, value):
        self.__haricot = value


    # -- Fonctionnalités --

    def verifPlante(self, position):
        for x in self.__emplacementDispo:
            if abs( position[0] - x ) <= 50:
                return True

        return False

    def getPlantePosition(self,position):
        for plante in self.__plantes:
            p = plante.position[0]
            if(abs(position[0] - p)<50):
                return plante
        return None

    # Plantes
    # {coordonné de la plante OK}=>{ajout au terrain}
    def addPlante(self, plante):
        plante.alignment = 'bottom-center'
        p = plante.position[0]

        i = 0
        while i < len(self.__emplacementDispo) and abs( p - self.__emplacementDispo[i] ) > 50:
            i += 1

        if i < len(self.__emplacementDispo):
            p = self.__emplacementDispo[i]

            plante.position = (p, plante.position[1])
            self.__emplacementDispo.remove(p)

            self.__plantes.append(plante)
            self.addSprite('main', plante)


    def removePlante(self,plante):
        self.__plantes.remove(plante)
        p = plante.position[0]
        for i in self.__emplacementTotal:
            if(abs(p-int(i))<50):
                self.__emplacementDispo.append(i)

        self.removeSprite('main', plante)

    # Soldats
    def addSoldat(self, soldat):
        if soldat.isAmi():
            self.amis.append(soldat)
        else:
            self.enemies.append(soldat)

        self.addSprite('main',soldat)

    def removeSoldat(self, soldat):
        if soldat.isAmi():
            self.amis.remove(soldat)
        else:
            for item in soldat.inventaire.get_indexs():
                self.__inventaire.add_contenu(item, soldat.inventaire.get_valeur_objet(item))

            self.enemies.remove(soldat)

        self.removeSprite('main', soldat)

    def openBoutique(self):
        # if la boutique n'est pas open (attr boutique ou terrain)
        if not self.__boutiqueOuverte:
            self.addSprite('main', self.__boutique)
            self.__boutiqueOuverte = True


    def closeBoutique(self):
        self.removeSprite('main', self.__boutique)
        self.__boutiqueOuverte = False

    def useTeq(self):
        if self.__isNight:
            soundTech = pygame.mixer.Sound("src/musics/effect/explosion.mp3")
            soundTech.play()
            self.__inventaire.soustraire_contenu('teq',1)
            ennemies = self.enemies.copy()
            for soldat in ennemies:
                self.removeSoldat(soldat)

    def loadSpriteManche(self, window):
        if(self.__manche > 9):
            images = []
            i = 0
            concat = str(self.__manche)
            for number in concat:
                images.append(Image((950 + 45 * (i-1), 35), 'src/images/chiffre/' + number + '.png'))
                images[i].alignment = "middle"
                images[i].size = (55,-1)
                window.addSprite('jeu', images[i])
                i += 1

            self.spritesChiffre[self.__manche] = images

        else:
            img = Image((950, 55), 'src/images/chiffre/' + str(self.__manche) + '.png')
            img.alignment = "middle"
            img.size = (55,-1)
            window.addSprite('jeu', img)
            self.spritesChiffre[self.__manche] = [ img ]

    def amiGeneration(self):
        if self.__isNight:
            # Génération des amis
            for plante in self.plantes:
                if(type(plante)==Cannabis):
                    count = int(plante.getNiveau() * plante.getPuissance())
                    direction = 'right'

                    if plante.position[0] <= 1024 / 2:
                        direction = 'left'

                    # Génération des amis
                    self.__ami_generation.append({ 'plante': plante, 'count': max(count, 1) })


    # -- Update --

    def update(self, window, parent_position = (0,0)):
        # Every time
        self.__joueur.action(self)

        if self.__boutiqueOuverte:
            self.__boutique.action(self)

        # Tests des combats
        enemies = self.enemies.copy()
        for enemy in enemies:
            if enemy.isLibre():

                # Plantes
                plantes = self.plantes.copy()
                for plante in plantes:
                    if type(plante) == Rose and abs(enemy.position[0] - plante.position[0]) < 10:
                        enemy.attaque(plante)

                        if plante.isDead():
                            self.removePlante(plante)
                            enemy.avance()

                # Amis
                amis = self.amis.copy()
                for ami in amis:
                    if ami.isLibre():
                        ami_x = ami.getRelPosition()[0]
                        enemy_x = enemy.position[0]

                        if ami_x < enemy_x and enemy_x < ami_x + ami.size[0]:
                            ami.combat(enemy)
                            randomHit = randint(1,4)
                            soundHit = pygame.mixer.Sound("src/musics/effect/hit/hit-"+str(randomHit)+".mp3")
                            soundHit.set_volume(0.1)
                            soundHit.play()

                            if ami.isDead():
                                self.removeSoldat(ami)
                        else:
                            ami.avance()


                if enemy.isDead():
                    self.removeSoldat(enemy)
                    pass

                if enemy.isLibre():
                    enemy.avance()
                    randomZiak = randint(1,100000)
                    if(randomZiak==1):
                        soundZiak = pygame.mixer.Sound("src/musics/effect/euh-ziak-1.mp3")
                        soundZiak.play()

                # Joueur
                if abs(enemy.position[0] - self.__joueur.position[0]) < 10:
                    soundFin = pygame.mixer.Sound("src/musics/effect/game-over.mp3")
                    soundFin.play()
                    window.stopSound()
                    window.runSound("src/musics/musique/end.mp3")
                    window.current_mode = 'defaite'

        # Suppression des amis sortis de la map
        amis = self.amis.copy()
        for ami in amis:
            ami_x = ami.getRelPosition()[0]
            if ami_x + ami.size[0] < -self.__max_left or ami_x > self.__max_left + 1024:
                self.removeSoldat(ami)

        # Finir la nuit
        if self.__isNight and len(self.enemies) == 0 and len(self.__enemy_generation) == 0:
            self.__isNight = False
            self.restartClock('transition.day')
            # set la video de transition de la journée
            self.__background.animate('transition.day', 'transition.day', 4)

            for soldat in self.amis:
                soldat.kill()
                soldat.stopAnimation()
                soldat.animate('dead', 'dead-end', 1)
                soldat.addAnimate('dead-end', 'dead-end',1)
            self.__ami_generation = []

        super().update(window, parent_position)


    def updateTime(self, window, clock, parent_position = (0,0)):
        if clock['name'] == 'manche':
            self.restartClock('transition.night')
            # set la video de transition de la nuit
            self.__background.animate('transition.night', 'transition.night', 4)

        elif clock['name'] == 'transition.day':
            self.__background.stopAnimation()
            self.__background.current_mode = 'day'

            # Suppr Amis
            amis = self.amis.copy()
            for soldat in amis:
                self.removeSoldat(soldat)
            self.__ami_generation = []

            for img in self.spritesChiffre[self.__manche]:
                window.removeSprite('jeu', img)

            self.__manche += 1
            self.loadSpriteManche(window)

            #self.__background.animate('main','main', max(30 - 0.1 * self.__manche, 1))
            self.restartClock('manche', max(30 - 0.1 * self.__manche, 1))

            # run sound
            window.stopSound()
            window.runSound("src/musics/musique/journee.mp3")

        elif clock['name'] == 'transition.night':
            # Set la nuit
            self.__isNight = True
            self.__background.stopAnimation()
            self.__background.current_mode = 'night'

            # Set sound
            window.stopSound()
            window.runSound("src/musics/musique/nuit.mp3")

            # Génération des amis
            self.amiGeneration()
            self.restartClock('cannabis')

            # Génération des enemys
            for i in range(0, self.__manche * 2):
                direction = 'left'
                position = ( self.__max_left + 1024, 768 - 166 )

                if( randint(0,1) == 0 ):
                    position  = ( -self.__max_left, 768 - 166 )
                    direction = 'right'

                self.__enemy_generation.append({ 'position': position, 'direction': direction })

        elif clock['name'] == 'cannabis':
            self.amiGeneration()

        elif clock['name'] == 'ami.generation':

            if len(self.__ami_generation) > 0:
                generation = self.__ami_generation.copy()
                for i in range(0, len(generation)):
                    data = generation[i]
                    plante = data['plante']

                    direction = 'right'

                    if plante.position[0] <= 1024 / 2:
                        direction = 'left'

                    ami = Soldat(self.joueur, True, 100, 10, (0, 768 - 166), None, direction)
                    ami.position = ( plante.position[0] + randint(-16,16), 768 - 166 )

                    ami.avance()
                    self.addSoldat(ami)

                    if data['count'] - 1 == 0:
                        self.__ami_generation.remove(generation[i])
                    else:
                        generation[i]['count'] -= 1

        elif clock['name'] == 'enemy.generation':

            if len(self.__enemy_generation) > 0:
                data = self.__enemy_generation[0]

                enemy = Soldat(self.__joueur, False, 100, 15 if self.__difficulte == 3 else 10, data['position'], Inventaire(100,"",(0,0)), data['direction'])

                self.addSoldat(enemy)
                enemy.avance()

                del self.__enemy_generation[0]

        elif clock['name'] == 'player.keys' or clock['name'] == 'player.moves':
            # Lancer les actions du player
            self.__joueur.actionTime(window, clock, self, parent_position)
