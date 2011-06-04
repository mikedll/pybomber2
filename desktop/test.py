#!/usr/bin/python2.3
import doctest

import pygame
from config import RESOLUTION, FLAGS
try:
    screen = pygame.display.set_mode(RESOLUTION, FLAGS)
except:
    pass

print "Testing map"
import map
doctest.testmod(map)

print "Testing gameworld"
import gameworld
doctest.testmod(gameworld)

print "Testing player"
import player
doctest.testmod(player)

print "Testing widget"
import widget
doctest.testmod(widget)

print "Testing color_picker"
import color_picker
doctest.testmod(color_picker)

