""" Allow each player to choose their color """

import pygame
from pygame.sprite import RenderUpdates as SpriteGroup
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.font import Font
from distutils import dir_util as d
from distutils import file_util as f
from config import *
import sys
from widget import *
from windows import *

ROWS = 2
COLUMNS = 7


class Swatch(Sprite):
    def __init__(self, color):
        Sprite.__init__(self)
        self.color = color
        self.image = pygame.surface.Surface((30, 30))
        self.image.fill(color)
        self.rect=Rect(0, 0, 30, 30)

    def setName(self, name):
        self.name = name


class Select(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load('images/selector.png').convert()
        self.image.set_colorkey(PUCE, RLEACCEL)
        self.rect=Rect(10, 10, 30, 30)
        self.index = 0

    def setX(self, x):
        newpos = (self.rect.topleft[0] + x)
        if (newpos > 0) and (newpos < COLUMNS * 40 + 10):
            self.rect.move_ip(x,0)
            if x > 0:
                self.index += 1
            else:
                self.index -= 1

    def setY(self, y):
        newpos = (self.rect.topleft[1] + y)
        if (newpos > 0) and (newpos < ROWS * 40 + 10):
            self.rect.move_ip(0, y)
            if y > 0:
                self.index += COLUMNS
            else:
                self.index -= COLUMNS


class ColorPicker:
    def __init__(self, default):
        self.default = default

    def switchColor(self, widget, swatches, i):
        colorOfPlayer = pygame.surface.Surface((500, 500))
        colorOfPlayer.fill(swatches[i].color)
        bomberStencil = pygame.image.load('images/BM_Stencil.png').convert()
        bomberStencil.set_colorkey(PUCE)
        colorOfPlayer.blit(bomberStencil, ((0, 0),(500, 500)))
        colorOfPlayer.set_colorkey(LAVENDER)
        colorOfPlayer = pygame.transform.scale(colorOfPlayer, (100, 100))
        widget.image = colorOfPlayer

    def createStrips(self, color, playerNo):
        # Create each regular players strip
        for direction in ("up","down","right","left"):
            colorOfPlayer = pygame.surface.Surface((1200, 200))
            colorOfPlayer.fill(color)
            bomberStencil = pygame.image.load('images/stencils/' + direction
                              + '/' + direction + '_strip.png').convert()
            bomberStencil.set_colorkey(LAVENDER)
            colorOfPlayer.blit(bomberStencil, ((0, 0),(1200, 200)))
            colorOfPlayer = pygame.transform.scale(colorOfPlayer,\
                                                   (6*BMANSIZE[0], BMANSIZE[1]))
            pygame.image.save(colorOfPlayer, "images/player" + str(playerNo)\
                              + "/" + direction + "_strip.bmp")

        # Create each shielded players strip
        for direction in ("up","down","right","left"):
            colorOfPlayer = pygame.surface.Surface((1200, 200))
            colorOfPlayer.fill(color)
            bomberStencil = pygame.image.load('images/stencils/' + direction
                              + '/' + direction + '_stripShield.png').convert()
            bomberStencil.set_colorkey(LAVENDER)
            colorOfPlayer.blit(bomberStencil, ((0, 0),(1200, 200)))
            colorOfPlayer = pygame.transform.scale(colorOfPlayer,\
                                                   (6*BMANSIZE[0], BMANSIZE[1]))
            pygame.image.save(colorOfPlayer, "images/player" + str(playerNo)\
                              + "/" + direction + "_stripShield.bmp")

    def pickColors(self, playerList):
        background = pygame.surface.Surface(RESOLUTION)

        # Create swatches
        SwatchesGroup = SpriteGroup()
        swatches = [Swatch((0, 0, 0)),
                    Swatch((127, 0, 0)),
                    Swatch((255, 0, 0)),
                    Swatch((0, 127, 0)),
                    Swatch((0, 255, 0)),
                    Swatch((0, 0, 127)),
                    Swatch((0, 0, 255)),                    
                    Swatch((127, 127, 0)),
                    Swatch((0, 127, 127)),
                    Swatch((127, 0, 127)),
                    Swatch((0, 255, 255)),
                    Swatch((255, 0, 255)),
                    Swatch((255, 255, 0)),
                    Swatch((255, 255, 255))
                    ]

        l = 0
        for swatch in swatches:
            swatch.setName = str(swatch.color[0]) + "/" + str(swatch.color[1])\
                             + "/" + str(swatch.color[2])
            swatch.rect=Rect(
                (l % COLUMNS) * 40 + 10,
                (l / COLUMNS) * 40 + 10,
                30, 30)
            SwatchesGroup.add(swatch)
            l += 1

        # Create text box to enter players' names
        inputRect = Rect((400, 75, 100, 30))
        theInput = TextInput(playerList[0].playerName, inputRect, 30)
        SwatchesGroup.add(theInput)

        if not self.default:
            # Create Bomberman pic
            BMRect = Rect((510, 190), (100, 100))
            BMSurf = pygame.surface.Surface((100, 100))
            BMPic = Widget(BMSurf, BMRect)
            SwatchesGroup.add(BMPic)

            # Create some text to prompt players to pick color
            text = TextBar("Choose color. ", (400, 20, 100, 30), 25)
            text2 = TextBar("Backspace and type Player Name. Press Enter. ",\
                            (400, 40, 100, 30), 25)
            SwatchesGroup.add(text)
            SwatchesGroup.add(text2)

            background = pygame.image.load('images/bgd_grass.jpg').convert()
            screen.blit(background, ((0, 0),RESOLUTION))
            theSelector = Select()
            cursor = SpriteGroup()
            theSelector.rect = Rect(10, 10, 30, 30)
            cursor.add(theSelector)

            SwatchesGroup.draw(screen)
            pygame.display.flip()

        # Use default colors
        if self.default:
            for player in playerList:
                newpath = "images/player" + str(player.name)
                try:
                    d.mkpath(newpath)
                    self.createStrips(player.color, player.name)
                except:
                    print "Could not create strips"
                    return

        # Else, let players select their colors
        else:
            for player in playerList:
                newpath = "images/player" + str(player.name)
                try:
                    d.mkpath(newpath)
                    self.createStrips(player.color, player.name)
                except:
                    print "Could not create strips"
                    return
                
                optionsChosen = False
                theInput.setText(player.playerName)
                while (not optionsChosen):
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            sys.exit()
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                sys.exit()
                            elif event.key == K_RIGHT:
                                theSelector.setX(40)
                            elif event.key == K_LEFT:
                                theSelector.setX(-40)
                            elif event.key == K_UP:
                                theSelector.setY(-40)
                            elif event.key == K_DOWN:
                                theSelector.setY(40)
                            elif event.key == K_BACKSPACE:
                                theInput.deleteChar()
                            elif (event.key >= K_0 and event.key <= K_z)\
                                  or event.key == K_SPACE:
                                theInput.appendChar(event.key)
                            elif event.key == K_RETURN: #return key
                                d.mkpath(newpath)
                                self.createStrips(\
                                    swatches[theSelector.index].color, \
                                    player.name)
                                player.playerName = theInput.getText()
                                player.setColor(\
                                    swatches[theSelector.index].color)
                                optionsChosen = True

                    self.switchColor(BMPic, swatches, theSelector.index)
                    SwatchesGroup.clear(screen, background)
                    cursor.clear(screen, background)
                    cursor.update()
                    SwatchesGroup.update()
                    dirty = SwatchesGroup.draw(screen) + cursor.draw(screen)
                    pygame.display.update(dirty)

