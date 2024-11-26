"""
Auteur : Beaufils Tao
"""

# PyGames
import pygame
from pygame.locals import *

# Personnels
from src.element import Element

class Window(Element):

    # -- Constructors --

    def __init__(self, size):
        super().__init__("accueil", (0,0))

        # Attrs
        self.__langue = 'fr'
        self.__active = True
        self.__pyWindow = pygame.display.set_mode(size)


    # -- Getters --

    @property
    def langue(self):
        return self.__langue

    @property
    def active(self):
        return self.__active

    @property
    def pyWindow(self):
        return self.__pyWindow



    # -- Setters --

    @langue.setter
    def langue(self, value):
        self.__langue = value

    @active.setter
    def active(self, value):
        self.__active = value

    @pyWindow.setter
    def pyWindow(self, value):
        self.__pyWindow = value


    # -- Update --
    def runSound(self,url):
        pygame.mixer.music.load(url)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)

    def stopSound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def checkEvent(self, window, event):
        if event.type == QUIT:
            self.active = False

        super().checkEvent(window, event)

    def update(self):
        super().update(self)

    def refresh(self):
        super().refresh(self)
        pygame.display.flip()
