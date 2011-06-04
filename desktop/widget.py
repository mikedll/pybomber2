import pygame
from pygame.surface import *
from pygame.sprite import Sprite
from pygame.sprite import RenderUpdates as SpriteGroup
from pygame.sprite import spritecollide
from pygame.sprite import spritecollideany
from pygame.rect import Rect
from random import *
from config import *
from log import *


screen = None

def createFrames(image):
    fr_width = image.get_height()
    fr_size = fr_width, fr_width
    frames = []
    for frame_no in range(0, image.get_width(), fr_width):
        frame = pygame.Surface(fr_size)
        frame.blit(image, (0,0), ((frame_no,0), fr_size))
        frame.set_colorkey(PUCE)
        frames.append(frame)
    return frames

def initPygame():
    pygame.init()
    global screen

    screen = pygame.display.set_mode(RESOLUTION, FLAGS)


class Widget(Sprite):
    """Use Widget class for better movement tracking

       Widget class inherits from Sprite class.
       Test cases for class Widget

       >>> from widget import *
       >>> import pygame
       >>> s = pygame.surface.Surface((30,30))
       >>> w = Widget(s, (0,0,30,30), (0,0))
       >>> w.rect
       <rect(0, 0, 30, 30)>
       >>> w.update()
       >>> w.rect
       <rect(0, 0, 30, 30)>
       >>> w.getMovement()
       [0, 0]

       >>> w.setX(1)
       >>> w.getX()
       1

       >>> w.setY(4)
       >>> w.getY()
       4

       >>> w.setMovement((3,5))
       >>> w.getMovement()
       (3, 5)

       >>> w.getName()
       (0, 0)

       >>> w.setPosition((5,7))
       >>> w.getPosition()
       (5, 7)
    """

    def __init__(self, image, rect, name=''):
        """Instantiate a widget with a given surface,
           rectangle, and (x,y) movement pair.
        """
        Sprite.__init__(self)
        self.movement = [0, 0]
        self.rect = Rect(rect)
        self.lastRect = self.rect
        self.image = image
        self.name = name
        self.frames = []
        self.frameIndex = 0
        self.frameRate = 1
        self.timeDelay = WIDGETFRAMES
        self.lastUpdate = 0
        self.world = None
        self.undone = False
        self.id = self.rect.top + self.rect.left +\
                  self.rect.width + self.rect.height

    def attachToWorld(self, world):
        self.world = world
        self.id = self.world.curWidgetID
        self.world.curWidgetID += 1

    def startAnimation(self, frames, startIndex, frameRate):
        self.frames = frames
        self.frameIndex = startIndex
        self.frameRate = frameRate
        self.image = self.frames[startIndex]
        self.lastUpdate = self.timeDelay

    def __str__(self):
        return str(self.rect.left) + str(self.rect.top) + str(self.id)

    def setMovement(self, vector):
        """Set movement with a pair"""
        if(self.movement != [0,0]
           and vector == [0,0]):
            self.world.dirtyGroup.add(self)
        self.movement = vector

    def getMovement(self):
        """Return movement as a pair"""
        return self.movement

    def setStop(self):
        """Set movement to 0"""
        self.setMovement([0,0])

    def setY(self, y):
        """Set y-component of movement"""
        self.movement[1] = y

    def setX(self, x):
        """Set x-component of movement"""
        self.movement[0] = x

    def getX(self):
        """Get x-component of movement"""
        return self.movement[0]
    def getY(self):
        """Set y-component of movement"""
        return self.movement[1]

    def setPosition(self, pair):
        """Set x and y coords of Widget"""
        self.rect.topleft = pair

    def getPosition(self):
        """Get x and y coords of Widget"""
        return self.rect.topleft

    def update(self):
        """Move sprite according to its movement vector"""
        # Widget needs to be animated
        if (len(self.frames) > 0):
            if self.lastUpdate <= 0:
                self.frameIndex = (self.frameIndex+1)%(len(self.frames))
                self.image = self.frames[self.frameIndex]
                self.lastUpdate = self.timeDelay
                self.world.dirtyGroup.add(self)
            else:
                self.lastUpdate -= 1

        elif(self.getMovement != [0,0]):
            self.lastRect = Rect(self.rect)
            self.rect.move_ip(self.movement)
            self.world.dirtyGroup.add(self)

    def undoUpdate(self):
        """Widget returns to state prior to last update()"""
        self.rect = self.lastRect

    def getShadow(self):
        shadow = Sprite()
        shadow.rect = self.lastRect.move(0,0)
        return shadow

    def getName(self):
        """Get name of Widget"""
        return self.name


class WorldlessWidget(Widget):
    def update(self):
        """Move sprite according to its movement vector"""
        # Widget needs to be animated
        if (len(self.frames) > 0):
            if self.lastUpdate <= 0:
                self.frameIndex = (self.frameIndex+1)%(len(self.frames))
                self.image = self.frames[self.frameIndex]
                self.lastUpdate = self.timeDelay

        self.lastRect = Rect(self.rect)
        self.rect.move_ip(self.movement)
