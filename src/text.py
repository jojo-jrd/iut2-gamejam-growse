"""
Auteur : Beaufils Tao
"""

# PyGames
import pygame
from pygame.locals import *

# Personnels
from src.element import Element
from src.image import Image

class Text(Element):

    # -- Constructors --

    def __init__(self, position, text, font_url, font_size = 14, color = (0, 0, 0)):
        super().__init__("main", position)

        self.font_url = font_url
        self.font_size = font_size
        self.color = color
        self.text = text
        self.__spritesChiffre = {}

    # -- Getters --

    @property
    def font_url(self):
        return self.__font_url

    @property
    def font_size(self):
        return self.__font_size

    @property
    def color(self):
        return self.__color

    @property
    def text(self):
        return self.__text

    # -- Setters --

    @font_url.setter
    def font_url(self, value):
        self.__font_url = value

    @font_size.setter
    def font_size(self, value):
        self.__font_size = value

    @color.setter
    def color(self, value):
        self.__color = value

    @text.setter
    def text(self, value):
        self.__text = value
        self.background = pygame.font.Font(self.__font_url, self.__font_size).render(value, True, self.__color)


    def loadManches(self,manche):
        if(manche > 9):
            images = []
            i = 0
            concat = str(manche)
            for number in concat:
                images.append(Image((51 + i*7,0), 'src/images/chiffre/' + number + '.png'))
                images[i].size = (-1,15)
                self.addSprite('main',images[i])
                i += 1

            self.__spritesChiffre[manche] = images
        else:
            img = Image((51,0), 'src/images/chiffre/' + str(manche) + '.png')
            img.size = (-1,15)
            self.addSprite('main',img)
            self.__spritesChiffre[manche] = [ img ]

    def setup_chiffre(self,manche):
        if manche in self.__spritesChiffre:
            for img in self.__spritesChiffre[manche]:
                self.removeSprite("main", img)

        self.loadManches(manche)
