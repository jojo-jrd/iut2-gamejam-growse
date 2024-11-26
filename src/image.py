"""
Auteur : Beaufils Tao
"""

# PyGames
import pygame
from pygame.locals import *

from src.animate_element import AnimateElement

# Personnels
from src.element import Element

class Image(AnimateElement):

    # -- Constructors --

    def __init__(self, position, url, size = (-1,-1), langue = 'fr'):
        super().__init__("main", position)

        self.__langue = langue
        self.__size = size

        self.url = url

    # -- Getters --

    @property
    def url(self):
        return self.__url

    # -- Setters --

    @url.setter
    def url(self, value):
        self.__url = value
        self.loadBackground(self.__url, self.__size, self.__langue)
