"""
Auteur : Beaufils Tao
"""

# PyGames
import pygame
from pygame.locals import *

# Personnels
from src.element import Element

class Button(Element):

    # -- Constructors --

    def __init__(self, position, callback):
        super().__init__("main", position)

        self.__callback = callback


    # -- Update --

    def checkEvent(self, window, event, parent_position = (0,0)):
        pos = self.getAbsPosition(parent_position)

        if event.type == MOUSEBUTTONDOWN:
            # Left click
            if event.button == 1:
                mouse = pygame.mouse.get_pos()
                size = self.size

                if pos[0] <= mouse[0] and mouse[0] <= pos[0] + size[0] and pos[1] <= mouse[1] and mouse[1] <= pos[1] + size[1]:
                    try:
                        self.__callback(window, self.getRelPosition())
                    except TypeError:
                        self.__callback(window)

        super().checkEvent(window, event, pos)
