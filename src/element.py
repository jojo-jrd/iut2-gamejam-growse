"""
Auteur : Beaufils Tao
"""

# STL
import time
from random import randint

# PyGames
import pygame
from pygame.locals import *

class Element:

    images = {} # <url, pyElement>

    # -- Constructors --

    def __init__(self, mode = 'main', position = (0,0)):
        self.__sprites = {}

        # Attrs
        self.__current_mode = mode
        self.__position = position
        self.__alignment = 'top-left'
        self.__direction = 'right'
        self.__size = (-1,-1)
        self.__langue = 'fr'
        self.__background = {}

        # Time
        self.__previous_time = time.time()
        self.__clocks = [] # <{ name: str, "max": float, "elapsed": float, "auto": bool, "done": bool }>


    # -- Properties --

    # Sprites
    @property
    def sprites(self):
        return self.__sprites

    # Mode
    @property
    def current_mode(self):
        return self.__current_mode

    # Position
    @property
    def position(self):
        return self.__position

    # Background
    @property
    def background(self):
        try:
            return self.__background[self.__langue]
        except KeyError:
            try:
                return self.__background['fr']
            except KeyError:
                raise AttributeError


    # Alignment
    @property
    def alignment(self):
        return self.__alignment

    # Size
    @property
    def width(self):
        width = self.__size[0]

        if width == -1:
            try:
                width = self.background.get_size()[0]
            except AttributeError:
                for sprite in self.getCurrentSprites():
                    width = max(sprite.width, width)

                if width == -1:
                    width = 0

        return width

    @property
    def height(self):
        height = self.__size[1]

        if height == -1:
            try:
                height = self.background.get_size()[1]
            except AttributeError:
                for sprite in self.getCurrentSprites():
                    height = max(sprite.height, height)

                if height == -1:
                    height = 0

        return height

    @property
    def size(self):
        width, height = self.__size

        if width == -1 or height == -1:
            try:
                bg_size = self.background.get_size()

                if width == -1:
                    width = bg_size[0]

                if height == -1:
                    height = bg_size[1]
            except AttributeError:
                sprites = self.getCurrentSprites()
                for sprite in sprites:
                    size = sprite.size

                    if width == -1:
                        width = max(size[0], width)

                    if height == -1:
                        height = max(size[1], height)

                if width == -1:
                    width = 0

                if height == -1:
                    height = 0

        return (width,height)

    # Direction
    @property
    def direction(self):
        return self.__direction

    # Current sprite
    def getCurrentSprites(self):
        if not self.__current_mode in self.__sprites:
            return []

        return self.__sprites[self.__current_mode]

    # Get position
    def getRelPosition(self):
        # Get size
        size = self.size

        # Update position with alignment
        if self.__alignment == 'top-center':
            return ( self.__position[0] - size[0] / 2, self.__position[1] )
        elif self.__alignment == 'top-right':
            return ( self.__position[0] - size[0]    , self.__position[1] )
        elif self.__alignment == 'middle':
            return ( self.__position[0] - size[0] / 2, self.__position[1] - size[1] / 2 )
        elif self.__alignment == 'bottom-center':
            return ( self.__position[0] - size[0] / 2, self.__position[1] - size[1] )
        elif self.__alignment == 'bottom-right':
            return ( self.__position[0] - size[0]    , self.__position[1] - size[1] )
        elif self.__alignment == 'bottom-left':
            return ( self.__position[0]              , self.__position[1] - size[1] )

        return self.__position

    def getAbsPosition(self, parent_position):
        rel_pos = self.getRelPosition()
        return (round(rel_pos[0] + parent_position[0]), round(rel_pos[1] + parent_position[1]))

    # -- Setters --

    # Mode
    @current_mode.setter
    def current_mode(self, value):
        self.__current_mode = value

        if not value in self.__sprites:
            self.__sprites[value] = []

    # Position
    @position.setter
    def position(self, value):
        self.__position = value

    # Background
    @background.setter
    def background(self, value):
        self.__background[self.__langue] = value

    # Alignment
    @alignment.setter
    def alignment(self, value):
        self.__alignment = value

        for mode in self.__sprites:
            for sprite in self.__sprites[mode]:
                sprite.alignment = value

    # Size
    @size.setter
    def size(self, value):
        self.__size = value

        try:
            if value != (-1,-1):
                size = self.background.get_size()
                width, height = value

                if value[0] == -1:
                    width  = round(value[1] / size[1] * size[0])

                if value[1] == -1:
                    height = round(value[0] / size[0] * size[1])

                for langue in self.__background:
                    self.__background[langue] = pygame.transform.scale(self.__background[langue], (width, height))
        except AttributeError:
            pass

        # Update sprites
        for mode in self.sprites:
            for sprite in self.sprites[mode]:
                sprite.size = value

    # Direction
    @direction.setter
    def direction(self, value):
        if self.direction != value:
            self.scale_x()

        self.__direction = value


    # -- Loadings --

    def loadBackground(self, url, size = (-1,-1), langue = 'fr'):
        if not url in Element.images:
            Element.images[url] = pygame.image.load(url).convert_alpha()

        self.__background[langue] = Element.images[url]
        self.size = size

    # -- Adding --

    def addSprite(self, mode, element):
        if not mode in self.__sprites:
            self.__sprites[mode] = []

        self.__sprites[mode].append(element)

    def removeSprite(self, mode, element):
        try:
            self.__sprites[mode].remove(element)
        except ValueError:
            pass

    def removeMode(self, mode):
        self.__sprites[mode] = []


    # -- Transform --

    def scale_x(self):
        if self.__direction == 'right':
            self.__direction = 'left'
        else:
            self.__direction = 'right'

        try:
            self.background = pygame.transform.flip(self.background, True, False)
        except AttributeError:
            pass

        # Update sprites
        for mode in self.sprites:
            for sprite in self.sprites[mode]:
                sprite.scale_x()


    # -- Time --

    def startClock(self, name, resetTime, auto = True, done = False):
        i = 0

        while i < len(self.__clocks) and self.__clocks[i]['name'] != name:
            i += 1

        if i == len(self.__clocks):
            self.__clocks.append({ 'name': name, 'resetTime': resetTime, 'elapsed': 0, 'auto': auto, 'done': done })

    def restartClock(self, name, resetTime = -1):
        i = 0

        while i < len(self.__clocks) and self.__clocks[i]['name'] != name:
            i += 1

        if i < len(self.__clocks):
            if resetTime != -1:
                self.__clocks[i]['resetTime'] = resetTime

            self.__clocks[i]['done'] = False
            self.__clocks[i]['elapsed'] = 0


    # -- Update --

    def checkEvent(self, window, event, parent_position = (0,0)):
        self.__langue = window.langue
        abs_pos = self.getAbsPosition(parent_position)

        # Check sprites
        sprites = self.getCurrentSprites()
        for sprite in sprites:
            sprite.checkEvent(window, event, abs_pos)

    def update(self, window, parent_position = (0,0)):
        self.__langue = window.langue
        abs_pos = self.getAbsPosition(parent_position)

        # Time
        current_time = time.time()
        elapsed = current_time - self.__previous_time

        for clock in self.__clocks:
            if not clock['done']:
                clock['elapsed'] += elapsed

                if clock['elapsed'] >= clock['resetTime']:
                    self.updateTime(window, clock, abs_pos)

                    clock['done'] = True
                    clock['elapsed'] = 0

                    if clock['auto']:
                        clock['done'] = False

        self.__previous_time = time.time()

        # Blit sprites
        sprites = self.getCurrentSprites()
        for sprite in sprites:
            sprite.update(window, abs_pos)

    def refresh(self, window, parent_position = (0,0)):
        abs_pos = self.getAbsPosition(parent_position)

        # Blit background
        try:
            window.pyWindow.blit(self.background, abs_pos)
        except AttributeError:
            pass

        # Blit sprites
        sprites = self.getCurrentSprites()
        for sprite in sprites:
            sprite.refresh(window, abs_pos)

    def updateTime(self, window, clock, parent_position = (0,0)):
        pass
