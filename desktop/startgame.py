#!/usr/bin/python2.3 -tt

"""Splash screen at game's start"""

import sys as s
import pygame
from pygame.sprite import RenderUpdates as SpriteGroup
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.font import Font
from config import *
import time as t
from widget import *


def createFrames(image):
    fr_width = image.get_height()
    fr_size = fr_width, fr_width
    frames = []
    for frame_no in range(0, image.get_width(), fr_width):
        frame = pygame.Surface(fr_size)
        frame.blit(image, (0,0), ((frame_no, 0), fr_size))
        frame.set_colorkey(PUCE)
        frames.append(frame)
    return frames

def startGame():
    background = pygame.surface.Surface(RESOLUTION)
    background = pygame.image.load(BACKGROUND).convert()
    screen.blit(background, ((0, 0),RESOLUTION))

    # Create title from image
    titleSize = ((int(RESOLUTION[0] * .75)), (int(RESOLUTION[0] * .3)))
    titleRect = Rect((0, 0), titleSize)
    titleRect.midtop = (screen.get_rect().centerx, 20)
    titleSurf = pygame.surface.Surface(titleSize)
    title = Widget(titleSurf, titleRect)
    tempImage = pygame.image.load('images/title.png').convert()
    tempImage = pygame.transform.scale(tempImage, titleSize)
    tempImage.set_colorkey(PUCE, RLEACCEL)
    title.image = tempImage

    # Create animated bomb on screen
    bombRect = Rect((0, 0), (200, 200))
    bombRect.centerx = screen.get_rect().centerx
    bombRect.centery = screen.get_rect().centery
    bombSurf = pygame.surface.Surface((200, 200))
    bomb = Widget(bombSurf, bombRect)
    tempImage = pygame.image.load('images/bomb/bomb_strip_title.png').convert()
    bombFrames = createFrames(tempImage)
    bomb.image = bombFrames[0]

    # Create 'Press any Key' message from image
    pressKeySize = ((int(RESOLUTION[0] * .75)), (int(RESOLUTION[0] * .15)))
    pressKeySurf = pygame.surface.Surface(pressKeySize)
    pressKeyRect = Rect((0, 0), pressKeySize)
    pressKeyRect.midbottom = screen.get_rect().midbottom
    pressKey = Widget(pressKeySurf, pressKeyRect)
    tempImage = pygame.image.load('images/press_key.png').convert()
    tempImage = pygame.transform.scale(tempImage, pressKeySize)
    tempImage.set_colorkey(PUCE, RLEACCEL)
    pressKey.image = tempImage

    myGroup = SpriteGroup()
    myGroup.add(title)
    myGroup.add(bomb)
    myGroup.add(pressKey)

    pygame.display.flip()

    i = 0
    MaxFR = 15
    lastUpdate = t.time()
    frameTime = 1.0 / float(MaxFR)
    while 1:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == JOYBUTTONDOWN:
                return
            if event.type == QUIT:
                s.exit()

        bomb.image = bombFrames[i]
        myGroup.clear(screen, background)
        myGroup.update()
        dirty = myGroup.draw(screen)
        pygame.display.update(dirty)
        if t.time() > lastUpdate + frameTime:
            i = (i+1) % 4
            lastUpdate = t.time()

