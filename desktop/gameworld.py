from time import sleep
from config import *
import pygame
from socket import *
from pygame.sprite import RenderUpdates as SpriteGroup
from pygame.sprite import Sprite
from pygame.sprite import spritecollideany
from pygame.sprite import spritecollide
import pygame.display as Display
from log import *


class GameWorld:
    """Hold Game World objects

       Initialize display
       >>> import pygame as pygame
       >>> import random
       >>> from widget import *
       >>> randomizer = Random()

       Create a gameworld
       >>> g = GameWorld(randomizer)
       >>> s = pygame.surface.Surface((30,30))
       >>> w = Widget(s, (0,0,30,30), (0,0))

       Add and test bomberman to world
       >>> g.appendBomber(w)
       >>> g.bomberGroup
       <RenderUpdates(1 sprites)>

       Add and test an immutable to world
       >>> w1 = Widget(s, (0,0,30,30), (0,0))
       >>> g.appendImmutable(w1)
       >>> g.immutableGroup
       <RenderUpdates(1 sprites)>

       Add another bomberman to world
       >>> p2 = Widget(s, (100,100, 30,30), (0,0))
       >>> g.appendBomber(p2)

       Add a bomb to the game world
       >>> bomb = Widget(s, (100,100,30,30), (0,0))
       >>> g.appendBomb(bomb)

       Check the number of objects in game world
       >>> g.universalGroup
       <RenderUpdates(4 sprites)>

       Detonate bomb in game world
       >>> g.detonateBomb(bomb)
       >>> g.bombGroup
       <RenderUpdates(0 sprites)>
       >>> g.universalGroup
       <RenderUpdates(3 sprites)>

       Add bomb to populatedBombGroup
       >>> g.appendPopulatedBomb(bomb)
       >>> g.populatedBombGroup
       <RenderUpdates(1 sprites)>

       Add an explosion to game world
       >>> explosion = Widget(s, (0,0,30,30),(0,0))
       >>> g.appendExplosion(explosion)
       >>> g.explosionGroup
       <RenderUpdates(1 sprites)>

       Add a power up to game world
       >>> powerup = Widget(s,(0,0,30,30),(0,0))
       >>> g.appendPowerUp(powerup)
       >>> g.powerUpGroup
       <RenderUpdates(1 sprites)>

       Remove power up from game world
       >>> g.removePowerUp(powerup)
       >>> g.powerUpGroup
       <RenderUpdates(0 sprites)>

       Test bomberstrafe algorithm
       >>> g.bomberStrafe([98, 100])
       (98, 100)

       >>> g.bomberStrafe([90, 100])
       (80, 100)

       >>> g.bomberStrafe([98, 90])
       (98, 80)

       >>> g.bomberStrafe([139, 140])
       (144, 144)

       Test worldWrap
       >>> g.mapColumns = 19
       >>> bomb = Bomb(s, (0,0,30,30),3,3,3,(0,0))
       >>> bomb.beingPunched = 1
       >>> g.appendBomb(bomb)
       >>> bomb.setPosition((10,100))
       >>> g.worldWrap(bomb)
       >>> bomb.getPosition()
       (624, 100)

       >>> bomb.setPosition((630,100))
       >>> g.worldWrap(bomb)
       >>> bomb.getPosition()
       (16, 100)

       >>> g.mapRows = 19
       >>> bomb.setPosition((100, 10))
       >>> g.worldWrap(bomb)
       >>> bomb.getPosition()
       (100, 656)

       >>> bomb.setPosition((100, 660))
       >>> g.worldWrap(bomb)
       >>> bomb.getPosition()
       (100, 48)

       Test for new restart game state
       >>> g.cleanState()
       >>> g.populatedBombGroup
       <RenderUpdates(0 sprites)>
       >>> g.bombGroup
       <RenderUpdates(0 sprites)>
       >>> g.bomberGroup
       <RenderUpdates(0 sprites)>
       >>> g.explosionGroup
       <RenderUpdates(0 sprites)>
       >>> g.immutableGroup
       <RenderUpdates(0 sprites)>
       >>> g.powerUpGroup
       <RenderUpdates(0 sprites)>
       >>> g.mutableGroup
       <RenderUpdates(0 sprites)>
       >>> g.universalGroup
       <RenderUpdates(0 sprites)>
       >>> g.dirtyGroup
       <RenderUpdates(0 sprites)>
       >>> g.flyOverGroup
       <RenderUpdates(0 sprites)>

       >>> g.update()
    """

    def __init__(self, randomizer):
        self.randomizer = randomizer

        # Set title
        pygame.display.set_caption("Pybomber")

        # Setup screen
        self.screen = pygame.display.get_surface()

        # Create sprite groups
        self.populatedBombGroup = SpriteGroup()
        self.bombGroup = SpriteGroup()
        self.bomberGroup = SpriteGroup()
        self.explosionGroup = SpriteGroup()
        self.immutableGroup = SpriteGroup()
        self.powerUpGroup = SpriteGroup()
        self.mutableGroup = SpriteGroup()
        self.universalGroup = SpriteGroup() # For drawing everything.
        self.dirtyGroup = SpriteGroup()
        self.flyOverGroup = SpriteGroup()
        # Load a background
        self.background = pygame.image.load(BACKGROUND).convert()
        self.map = None

        # Draw background on screen
        self.screen.blit(self.background, ((0, 0), RESOLUTION))

        # Number of rows and colums in the current map.
        self.mapRows = 0
        self.mapColumns = 0

    def cleanState(self):
        pygame.display.set_caption("Pybomber")
        self.screen.blit(self.background, ((0, 0), RESOLUTION))

        self.populatedBombGroup = SpriteGroup()
        self.bombGroup = SpriteGroup()
        self.bomberGroup = SpriteGroup()
        self.explosionGroup = SpriteGroup()
        self.immutableGroup = SpriteGroup()
        self.powerUpGroup = SpriteGroup()
        self.mutableGroup = SpriteGroup()
        self.universalGroup = SpriteGroup() # For drawing everything.
        self.dirtyGroup = SpriteGroup()
        self.groundGroup = SpriteGroup()
        self.flyOverGroup = SpriteGroup()
        self.mapRows = 0
        self.mapColumns = 0
        self.curWidgetID = 0

    def appendBomb(self, sprite):
        self.bombGroup.add(sprite)
        self.universalGroup.add(sprite)
        self.groundGroup.add(sprite)

    def flyBomb(self, bombSprite):
        self.groundGroup.remove(bombSprite)

    def groundBomb(self, bomb):
        self.groundGroup.add(bomb)

    def appendPopulatedBomb(self, sprite):
        self.populatedBombGroup.add(sprite)

    def appendExplosion(self, sprite):
        self.explosionGroup.add(sprite)
        self.universalGroup.add(sprite)

    def appendImmutable(self, sprite):
        self.flyOverGroup.add(sprite)
        self.immutableGroup.add(sprite)
        self.universalGroup.add(sprite)
        self.groundGroup.add(sprite)

    def appendBomber(self, sprite):
        self.bomberGroup.add(sprite)
        self.universalGroup.add(sprite)
        self.groundGroup.add(sprite)

    def appendPowerUp(self, sprite):
        self.powerUpGroup.add(sprite)
        self.universalGroup.add(sprite)

    def appendMutable(self, sprite):
        self.flyOverGroup.add(sprite)
        self.mutableGroup.add(sprite)
        self.universalGroup.add(sprite)
        self.groundGroup.add(sprite)

    def detonateBomb(self, bomb):
        """Detonate bomb"""
        bomb.kill()

    def removeExplosion(self, explosion):
        """Remove explosion from all groups."""
        self.explosionGroup.remove(explosion)
        self.universalGroup.remove(explosion)

    def removeBomber(self, bomber):
        """Remove explosion from all groups."""
        self.bomberGroup.remove(bomber)
        self.groundGroup.remove(bomber)
        self.universalGroup.remove(bomber)

    def removePopulatedBomb(self, sprite):
        self.populatedBombGroup.remove(sprite)

    def removePowerUp(self, powerUp):
        """Remove powerUp from all groups."""
        self.powerUpGroup.remove(powerUp)
        self.universalGroup.remove(powerUp)

    def bomberStrafe(self, bomberPos):
        """Take bomberman's position and find the nearest grid square."""
        posX = 0
        posY = 0

        # Get the location between grid.
        posBetweenGridX = (bomberPos[X]-XOFFSET) % BLOCKSIZE[X]
        posBetweenGridY = (bomberPos[Y]-YOFFSET) % BLOCKSIZE[Y]

        # If location is less than 1/3 way, move back,
        # if over 2/3, move forward.
        inMiddleX = (BLOCKSIZE[X]/3,2 * BLOCKSIZE[X]/3)
        inMiddleY = (BLOCKSIZE[Y]/3,2 * BLOCKSIZE[Y]/3)

        # Fix x
        if posBetweenGridX <= inMiddleX[0]:
            posX = bomberPos[X] - posBetweenGridX
        # Please leave the 0 and 1, they don't mean X and Y.
        elif(posBetweenGridX > inMiddleX[0] and\
             posBetweenGridX < inMiddleX[1]):
            posX = bomberPos[X]
        else: # > inMiddle[1]
            posX = bomberPos[X] + (BLOCKSIZE[X] - posBetweenGridX)

        # Fix y
        if posBetweenGridY <= inMiddleY[0]:
            posY = bomberPos[Y] - posBetweenGridY
        elif posBetweenGridY > inMiddleY[0] and\
             posBetweenGridY < inMiddleY[1]:
            posY = bomberPos[Y]
        else: # > inMiddleY[1]
            posY = bomberPos[Y] + (BLOCKSIZE[Y] - posBetweenGridY)

        return posX, posY

    def snapToGrid(self, pos):
        """Take position and find the nearest grid square."""
        posX = posY = 0
        # Get the location between grid.
        posBetweenGridX = (pos[0]-XOFFSET) % BLOCKSIZE[0]
        posBetweenGridY = (pos[1]-YOFFSET) % BLOCKSIZE[1]
        # If location is less than 1/2 way, move back, else move forward.
        if posBetweenGridX <= BLOCKSIZE[X]/2:
            posX = pos[X] - posBetweenGridX
        else:
            posX = pos[X] + (BLOCKSIZE[X] - posBetweenGridX)
        if posBetweenGridY <= BLOCKSIZE[Y]/2:
            posY = pos[Y] - posBetweenGridY
        else:
            posY = pos[Y] + (BLOCKSIZE[Y] - posBetweenGridY)
        return posX, posY

    def worldWrap(self, bomb):
        """Send bomb to other side of world if it was punched out of bounds
        """
        x, y = bomb.getPosition()
        if bomb.beingPunched:
            # Check top
            if y < YOFFSET:
                bomb.setPosition((x, self.mapRows*BLOCKSIZE[Y] + YOFFSET))
            # Check bottom
            if y > self.mapRows*BLOCKSIZE[Y] + YOFFSET:
                bomb.setPosition((x, YOFFSET))
            # Check left
            if x < XOFFSET:
                bomb.setPosition((self.mapColumns*BLOCKSIZE[X] + XOFFSET, y))
            # Check right
            if x > self.mapColumns*BLOCKSIZE[X] + XOFFSET:
                bomb.setPosition((XOFFSET, y))

    def update(self):
        """Update sprites in enviornment class

           Attempt to move each sprite, undoing movements
           that produce collisions.
        """
        explosionsToSort = self.explosionGroup.sprites()
        explosionsToSort.sort(lambda x, y: cmp(str(x), str(y)))
        for explosion in explosionsToSort:
            debug(str(explosion.rect.topleft) + " ")
            explosion.update()

        # Update players
        bombersToSort = self.bomberGroup.sprites()
        bombersToSort.sort(lambda x, y: cmp(x.id, y.id))
        for bomber in bombersToSort:
            bomber.update()

        # Update bombs
        bombsToSort = self.bombGroup.sprites()
        bombsToSort.sort(lambda x, y: cmp(x.id, y.id))
        for bomb in bombsToSort:
            bomb.update()

        # Update power-ups
        powerupSorted = self.powerUpGroup.sprites()
        powerupSorted.sort(lambda x, y: cmp(x.id, y.id))
        for powerup in powerupSorted:
            powerup.update()
