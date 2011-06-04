from widget import *
from powerup import *

expl_image_array = None
EXPL_FRAMES = None

class Explosion(Widget):
    def __init__(self, image, rect, TTL, napalm, radius, direction,
                 name, gameworld):
        global expl_image_array, EXPL_FRAMES
        if expl_image_array == None:
            expl_image_array = pygame.image.load('images/expl_anim.png')

            try:
                expl_image_array = expl_image_array.convert()
            except:
                pass
            EXPL_FRAMES = createFrames(expl_image_array)
            
        Widget.__init__(self, image, rect, name)

        self.world = gameworld
        self.id = self.world.curWidgetID
        self.world.curWidgetID += 1

        self.radius = radius
        self.direction = direction
        self.done = False
        self.napalm = napalm
        self.TTL = TTL
        self.frameIndex = 0

        # Grab images from global
        self.frames = EXPL_FRAMES
        self.image = self.frames[self.frameIndex]


    def tryToPropagate(self, direction=(0, 0)):
        """Create explosion in given direction if
           the way is not blocked by an immutable object
        """
        explosionRect = self.rect.move(direction[X] * BLOCKSIZE[X],
                                       direction[Y] * BLOCKSIZE[Y])
        explosion = Explosion(self.image, explosionRect, EXPLOSIONTTL,
                              self.napalm, self.radius - 1, direction,
                              self.name, self.world)

        if spritecollideany(explosion, self.world.immutableGroup) != None:
            return

        # If this collides with player with protection > 0, don't propagate
        protectedBombers = SpriteGroup()
        for bomber in self.world.bomberGroup.sprites():
            if bomber.protection > 0:
                protectedBombers.add(bomber)

        protectedbombers = spritecollide(explosion, protectedBombers, 0)
        protectedbombers.sort(lambda x, y: cmp(x.id, y.id))
        for bomber in protectedbombers:
            # Bomberman shield facing bomb blast!
            if bomber.direction == LEFT and explosion.direction == (1, 0)\
               or bomber.direction == RIGHT and explosion.direction == (-1,0)\
               or bomber.direction == UP and explosion.direction == (0, 1)\
               or bomber.direction == DOWN and explosion.direction == (0,-1):

                bomber.decrementProtection()
                bomber.animatePlayer()

            else:
               # Kill bomberman!
               self.world.appendExplosion(explosion)

            if bomber.protection <= 0:
                protectedBombers.remove(bomber)

        if len(protectedbombers) == 0:
            self.world.appendExplosion(explosion)

    def dyingSound(self):
        try:
            self.DS.play(0)
        except:
            pass

    def update(self):
        self.frameIndex = ((self.frameIndex + 1) % 16)
        self.image = self.frames[len(self.frames) - 1 - self.frameIndex]
        self.world.dirtyGroup.add(self)

        self.TTL -= 1
        if self.TTL == 0:
            self.world.removeExplosion(self)

        KILL = 1
        DONTKILL = 0

        # Destroy any and all powerups that the exlposion collided with.
        # Shouldn't be any more than one at most
        if self.napalm == 0:
            powerUp = spritecollideany(self, self.world.powerUpGroup)
            if powerUp != None:
                powerUp.kill()
                self.done = True

        # Kill blocks that the explosion collided with
        # >>>>>  SHOULD BE MAX OF ONE <<<<<
        deadBlock = spritecollideany(self, self.world.mutableGroup)
        if deadBlock != None:
            debug(str(deadBlock.rect.topleft) +\
                  str(deadBlock.id) +\
                  str("  was returned from ..any()"))
            deadBlock.kill()
            self.createPowerUp(deadBlock)

        # Kill players that the exlposion collided with.
        killables = spritecollide(self, self.world.bomberGroup, DONTKILL)
        killables.sort(lambda x, y: cmp(x.id, y.id))
        for k in killables:
            k.kill()
            # Play death sound
            self.dyingSound()

        # Detonate bombs the explosion colided with.
        # Do this by setting the time to live on each bomb to 1.
        bombs = spritecollide(self, self.world.bombGroup, DONTKILL)
        bombs.sort(lambda x, y: cmp(x.id, y.id))
        if len(bombs) != 0:
            if self.napalm == 0:
                self.done = True
            for b in bombs:
                b.setTTL(1)

        # If the explosion is not done, then try to propagate it.
        if(not self.done and self.world.explosionGroup.has(self)
           and self.radius > 0):
            if self.direction == (0, 0):
                self.tryToPropagate((1,0))  # Right
                self.tryToPropagate((-1,0)) # Left
                self.tryToPropagate((0,1))  # Up
                self.tryToPropagate((0,-1)) # Down
            else:
                self.tryToPropagate(self.direction)
            self.done = True

    def createPowerUp(self, deadBlock):
        """Randomly create a powerup"""
        
        randNum = self.world.randomizer.randint(1,200)
        powerUpRect = Rect(((deadBlock.getPosition()), BLOCKSIZE))
        powerUpKind = ''
        for i in POWERUPS.keys():
            if randNum <= POWERUPS[i]:
                powerUpKind = i
                break
            else:
                randNum -= POWERUPS[i]

        if(powerUpKind != ''):
            debug(str(randNum) +\
                  " was used to create this powerup.")
            powerUp = PowerUp(powerUpRect, powerUpKind)
            self.world.appendPowerUp(powerUp)
            powerUp.attachToWorld(self.world)
            if not self.napalm:
                self.world.removeExplosion(self)

        # If explosion sprite is napalm,
        # don't stop at a powerup
        if not self.napalm:
            self.done = True
