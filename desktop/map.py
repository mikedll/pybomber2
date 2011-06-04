import pygame
from random import *
from config import *
from widget import *
from error import *
from bomber import *
from powerup import *



class Map:
    def __init__(self, mapFile, gameworld, playerList):
        """Load a map."""

        self.grid = [[]]
        self.capacity = 0
        immutable = pygame.image.load('images/rock.png').convert()
        mutable = pygame.image.load('images/bricks32-32.png').convert()
        self.respawnPoints = []

        try:
            mapLineList = []
            f = open(mapFile, 'r')
            mapLineList = f.readlines()
            maxPlayers = int(mapLineList[0][0]) + 1
        except:
            raise MapNotLoaded

        self.capacity = 0
        
        # Map file cannot contain more than
        # COLUMNS letter(s) in each line
        for i in mapLineList:
            if len(i) > COLUMNS + 2:
                raise MapCapacityOverflow

        # Map file cannot contain more than
        # ROWS lines of letters
        if len(mapLineList) > ROWS + 1:
            raise MapCapacityOverflow

        # Map is now loaded and checked.
        self.capacity = int(mapLineList[0][0]) + 1
        mapLineList.pop(0)
        self.mapRows = len(mapLineList)
        self.mapColumns = len(mapLineList[0]) - 1

        # Create blocks map from file
        for y in range(-1, self.mapRows + 1):
            for x in range(-1, self.mapColumns + 1):
                # Create default immutable block border
                if y == -1 or y == self.mapRows or\
                   x == -1 or x == self.mapColumns:
                    blockPos = x*BLOCKSIZE[X] + XOFFSET,\
                                (y+1)*BLOCKSIZE[Y] + XOFFSET
                    blockRect = Rect(((blockPos), BLOCKSIZE))
                    block = Widget(immutable, blockRect)
                    gameworld.appendImmutable(block)
                    block.attachToWorld(gameworld)

        # Create wigdets from file
        for x in range(0, self.mapRows):
            thisGrid = []
            for y in range(0, self.mapColumns):
                thisGrid.append(None)
                # For immutable blocks
                blockPos = y*BLOCKSIZE[X] + XOFFSET,\
                            (x+1)*BLOCKSIZE[Y] + XOFFSET
                blockRect = Rect(((blockPos), BLOCKSIZE))     
                if mapLineList[x][y] == 'I':
                    block = Widget(immutable, blockRect)
                    gameworld.appendImmutable(block)
                    block.attachToWorld(gameworld)
                # For mutable blocks
                elif mapLineList[x][y] == 'M' or \
                     (mapLineList[x][y] == 'R' and\
                      gameworld.randomizer.randint(1,100) <= DENSITYMUTABLE):
                    block = Widget(mutable, blockRect)
                    gameworld.appendMutable(block)
                    block.attachToWorld(gameworld)
                # Power-ups
                elif mapLineList[x][y] in POWERUPMAP.keys():
                    powerUp = PowerUp(blockRect, POWERUPMAP[mapLineList[x][y]])
                    gameworld.appendPowerUp(powerUp)
                    powerUp.attachToWorld(gameworld)
                # For bombers
                elif mapLineList[x][y] in PLAYERPOS:
                    bomberPos = blockPos
                    self.respawnPoints.append(bomberPos)
                    if len(playerList) > int(mapLineList[x][y]):
                        bomberRect = Rect(((bomberPos), BMANSIZE))
                        player = playerList[int(mapLineList[x][y])]
                        bomber = Bomber(mutable, bomberRect, player)
                        gameworld.appendBomber(bomber)
                        bomber.attachToWorld(gameworld)
            self.grid.append(thisGrid)

        gameworld.mapRows = self.mapRows
        gameworld.mapColumns = self.mapColumns
        gameworld.map = self


    def getGrid(self):
        """Return a grid of objects
           for this map.
        """
        return None

    def getAt(self, row, column):
        """Return an object at a given cordinate
           in the map.
        """
        return None

    def getCapacity(self):
        return self.capacity

    def getRespawnPoints(self):
        return self.respawnPoints


class PureMap:
    def __init__(self):
        self.blockSize = 1

    def setBlockSize(self, n):
        self.blockSize = n

    def getCoords(self, position=(0, 0)):
        """
           Get x-y coordinates relative to player's
           position.

           >>> from map import *
           >>> a = PureMap()
           >>> a.blockSize
           1
           >>> a.setBlockSize(32)
           >>> a.blockSize
           32
           >>> a.getCoords((0,0))
           [0, 0]
           >>> a.getCoords((5,5))
           [0, 0]
           >>> a.getCoords((16,16))
           [1, 1]
           >>> a.getCoords((15,15))
           [0, 0]
           >>> a.getCoords((0,16))
           [0, 1]
           >>> a.getCoords((16,0))
           [1, 0]
           >>> a.getCoords((600,345))
           [19, 11]
        """

        return [self.getCoord(position[0]),
                self.getCoord(position[1])]

    def getCoord(self, position):
        """Get nearest block position for a single dimension
           position.

           >>> from map import *
           >>> a = PureMap()
           >>> a.setBlockSize(32)
           >>> a.getCoord(0)
           0
           >>> a.getCoord(1)
           0
           >>> a.getCoord(15)
           0
           >>> a.getCoord(16)
           1
        """

        moddedPosition = position % self.blockSize
        if(moddedPosition >= self.blockSize / 2):
            return position / self.blockSize + 1
        else:
            return position / self.blockSize

