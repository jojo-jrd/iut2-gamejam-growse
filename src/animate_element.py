"""
Auteur : Beaufils Tao
"""

# STL
import time

# PyGames
import pygame
from pygame.locals import *

# Personnels
from src.element import Element

class AnimateElement(Element):

    # -- Constructors --

    def __init__(self, mode = 'main', position = (0,0)):
        super().__init__(mode, position)

        self.__moves = [] # Contain { position: tuple, time: int, begin_position: tuple, "scale": bool }
        self.__animate_frames = [] # Contain { current: mode, end: mode, time: int, step: int, infinite }

        self.__previous_time = time.time()
        self.__elapsed = 0

    # -- Tests --

    def isMoving(self):
        return len(self.__moves) > 0

    def isAnimate(self):
        return len(self.__animate_frames) > 0

    def hasAnimation(self, name):
        return len(self.__animate_frames) > 0 and self.__animate_frames[0]['current'] == name


    # -- Setters --

    def moveTo(self, position, time, scale = True):
        self.__moves = [ { "position": position, "time": time, "begin": self.position, "scale": scale } ]

    def addMoveTo(self, position, time):
        return

    def stopMove(self):
        self.__moves = []

    def animate(self, current, end, time, infinite = False):
        self.__animate_frames = [ { "current": current, "end": end, "time": time, "step": 0, "infinite": infinite } ]
        self.__elapsed = 0

    def addAnimate(self, current, end, time, infinite = False):
        self.__animate_frames.append({ "current": current, "end": end, "time": time, "step": 0, "infinite": infinite })
        self.__elapsed = 0

    def stopAnimation(self):
        self.__animate_frames = []

    # -- Update --

    def update(self, window, parent_position = (0,0)):
        current_time = time.time()
        small_elapsed = current_time - self.__previous_time
        self.__elapsed += small_elapsed
        self.__previous_time = time.time()

        if self.isMoving():
            moving = self.__moves[0]
            end = (moving["begin"][0] + moving["position"][0], moving["begin"][1] + moving["position"][1])

            if moving["scale"]:
                if moving['position'][0] < 0:
                    self.direction = 'left'
                else:
                    self.direction = 'right'

            translate_x = small_elapsed / moving["time"] * moving["position"][0]
            translate_y = small_elapsed / moving["time"] * moving["position"][1]
            if abs(translate_x) > abs(end[0] - self.position[0]):
                translate_x = end[0] - self.position[0]

            if abs(translate_y) > abs(end[1] - self.position[1]):
                translate_y = end[1] - self.position[1]

            position = (self.position[0] + translate_x, self.position[1] + translate_y)
            if position == end:
                del self.__moves[0]

            self.position = position


        abs_pos = self.getAbsPosition(parent_position)
        if self.isAnimate():
            animation = self.__animate_frames[0]
            self.current_mode = animation['current']
            step = animation['step']
            updating = False

            if len(self.getCurrentSprites()) > 0 and self.__elapsed >= self.__animate_frames[0]['time'] / len(self.getCurrentSprites()):
                if step < len(self.getCurrentSprites()) - 1:
                    animation['step'] += 1
                    self.__elapsed = 0
                    updating = True
                else:
                    if animation['infinite']:
                        animation['step'] = 0

                        copy = animation['current']
                        animation['current'] = animation['end']
                        animation['end'] = copy

                        self.__elapsed = 0
                    else:
                        del self.__animate_frames[0]

        super().update(window, parent_position)

    def refresh(self, window, parent_position = (0,0)):
        abs_pos = self.getAbsPosition(parent_position)

        if self.isAnimate():
            step = self.__animate_frames[0]['step']

            # Blit background
            try:
                window.blit(self.background, abs_pos)
            except AttributeError:
                pass

            # Blit sprites
            self.sprites[self.current_mode][step].refresh(window, abs_pos)
        else:
            super().refresh(window, parent_position)
