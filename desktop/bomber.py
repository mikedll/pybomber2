from widget import *


class Bomber(Widget):
    """Test cases for class Bomber

       >>> from widget import *
       >>> from player import *
       >>> import pygame
       >>> s = pygame.surface.Surface((30,30))
       >>> player = Player("0", "Player0", 0)
       >>> b = Bomber(s, (0,0,30,30), player)
       >>> b.rect
       <rect(0, 0, 30, 30)>
    """

    def __init__(self, image, rect, player):
        Widget.__init__(self, image, rect, player)
        self.player = player
        self.name = player.name
        self.color = player.color

        # Default values
        self.capacity = STARTCAPACITY
        self.invulnerability = INVULNERABILITY
        self.radius = STARTRADIUS
        self.speed = BMANSPEED
        self.TTL = BOMBTTL
        # CommandSet is used for Confusion Virus
        self.player.commandSet = COMMANDSET[0]

        # Viruses
        self.virusDict = {RUNS: 0,
             CONFUSION: 0,
             CONSTIPATION: 0,
             SHORTFUSE: 0,
             SHORTRADIUS: 0,
             TURTLE: 0}

        # Powerups
        self.napalm = 0
        self.protection = 0
        self.kick = False
        #self.kick = True
        self.punch = False
        self.detonateEnable = False

        # Animation
        self.timeDelay = WIDGETFRAMES
        self.last_update = self.timeDelay

        # Regular animation strips
        self.path = 'images/player' + self.player.name + '/'
        self.down = pygame.image.load(self.path + 'down_strip.bmp')
        self.up = pygame.image.load(self.path + 'up_strip.bmp')
        self.left = pygame.image.load(self.path + 'left_strip.bmp')
        self.right = pygame.image.load(self.path + 'right_strip.bmp')

        # Shield animation strips
        self.downShield = pygame.image.load(self.path + \
                                            'down_stripShield.bmp')
        self.upShield = pygame.image.load(self.path + \
                                          'up_stripShield.bmp')
        self.leftShield = pygame.image.load(self.path + \
                                            'left_stripShield.bmp')
        self.rightShield = pygame.image.load(self.path + \
                                             'right_stripShield.bmp')

        try:
            self.down = self.down.convert()
            self.up = self.up.convert()
            self.left = self.left.convert()
            self.right = self.right.convert()
            self.downShield = self.downShield.convert()
            self.upShield = self.upShield.convert()
            self.leftShield = self.leftShield.convert()
            self.rightShield = self.rightShield.convert()

        except:
            pass

        self.frameIndex = 2
        self.down_frames = self.createFrames(self.down)
        self.up_frames = self.createFrames(self.up)
        self.left_frames = self.createFrames(self.left)
        self.right_frames = self.createFrames(self.right)

        self.down_framesShield = self.createFrames(self.downShield)
        self.up_framesShield = self.createFrames(self.upShield)
        self.left_framesShield = self.createFrames(self.leftShield)
        self.right_framesShield = self.createFrames(self.rightShield)

        self.image = self.down_frames[self.frameIndex]
        self.direction = DOWN
        self.moving = False

    # Create frames for animation
    def createFrames(self, image):
        fr_width = image.get_height()
        fr_size = fr_width, fr_width
        frames = []
        for frame_no in range(0, image.get_width(), fr_width):
            frame = pygame.Surface(fr_size)
            frame.blit(image, (0, 0), ((frame_no, 0), fr_size))
            frame.set_colorkey(PUCE)
            frames.append(frame)# .convert())
        return frames

    # For powerups!
    def decrementProtection(self):
        if self.protection > 0:
            self.protection -= 1

    def decrementNapalm(self):
        if self.napalm > 0:
            self.napalm -= 1

    def update(self):
        """Move sprite according to its movement vector"""

        # Decrement virus TTL
        for i in self.virusDict.keys():
            if self.virusDict[i] > 0:
                self.virusDict[i] -= 1

        # Special case for Confusion
        if self.virusDict[CONFUSION] == 0:
            self.virusDict[CONFUSION] = -1
            self.player.commandSet = COMMANDSET[0]

        # Decrement invulnerability
        if self.invulnerability > 0:
            self.invulnerability -= 1

        # Facing and animation
        self.faceBomber()
        if self.moving:
            self.animatePlayer()

        # Move bomber
        self.lastRect = Rect(self.rect)
        self.rect.move_ip(self.movement)
        self.world.dirtyGroup.add(self)

        # Check overlaping with other players for passing on of viruses
        otherBombers = []
        otherBombers = spritecollide(self, self.world.bomberGroup, 0)
        otherBombers.sort(lambda x, y: cmp(x.id, y.id))

        for otherBomber in otherBombers:
            if self != otherBomber:
                # If bomber has a virus and other bomber doesn't,
                # pass it on
                for i in self.virusDict.keys():
                    if self.virusDict[i] > 0 and otherbomber.virusDict[i] == 0:
                        otherBomber.virusDict[i] = VIRUSTTL
                        # Special case for Confusion
                        if self.virusDict[i] == CONFUSION:
                            self.player.commandSet = COMMANDSET[1]

        # Check colisions with powerUps
        powerUps = spritecollide(self, self.world.powerUpGroup, 0)
        powerUps.sort(lambda x, y: cmp(str(x), str(y)))
        for powerUp in powerUps:
            if powerUp.getPosition()[X] in range(
              self.getPosition()[X]-int(BLOCKSIZE[X] * WALKOVERCOVERAGE),
              self.getPosition()[X]+int(BLOCKSIZE[X] * WALKOVERCOVERAGE)) and \
              powerUp.getPosition()[Y] in range(
              self.getPosition()[Y]-int(BLOCKSIZE[Y] * WALKOVERCOVERAGE),
              self.getPosition()[Y]+int(BLOCKSIZE[Y] * WALKOVERCOVERAGE)):
                randNum = self.world.randomizer.randint(0, len(VIRUSLIST)-1)
                powerUp.activate(self, randNum)
                # Remove powerUp that the player picked up
                debug("Player " + self.name +\
                      " picked up " + powerUp.kind + "\n")
                self.world.removePowerUp(powerUp)

        # Undo move if hit block
        immutable = spritecollideany(self, self.world.immutableGroup)
        if immutable != None:
            self.undoUpdate()
            self.setPosition(self.world.bomberStrafe(self.getPosition()))

        # Undo move if hit brick
        mutable = spritecollideany(self, self.world.mutableGroup)
        if mutable != None:
            self.undoUpdate()
            self.setPosition(self.world.bomberStrafe(self.getPosition()))

        # Undo move if hit bomb
        bombs = spritecollide(self, self.world.bombGroup, 0)
        bombs.sort(lambda x, y: cmp(x.id, y.id))
        for bomb in bombs:
            peepsOnBomb = bomb.getPlaced()
            onBombWhenSet = False
            for peep in peepsOnBomb:
                # Was peep on the bomb when it was set?
                # If so, then let the peep get off!
                if(peep == self):
                    onBombWhenSet = True
                    break
            if(not onBombWhenSet):
                if self.kick and not bomb.beingPunched:
                    movement = self.getMovement()[X] * 1.5,\
                               self.getMovement()[Y] * 1.5
                    bomb.setMovement(movement)
                if self.punch and\
                    self.player.cachedCommand == ACTION:
                    position = movement = None
                    if self.direction == RIGHT:
                        movement = MAXBMANSPEED, 0
                        position = bomb.getPosition()[X] + 2*BLOCKSIZE[X],\
                                   bomb.getPosition()[Y]
                    elif self.direction == LEFT:
                        movement = -MAXBMANSPEED, 0
                        position = bomb.getPosition()[X] - 2*BLOCKSIZE[X],\
                                   bomb.getPosition()[Y]
                    elif self.direction == UP:
                        movement = 0, -MAXBMANSPEED
                        position = bomb.getPosition()[X],\
                                   bomb.getPosition()[Y] - 2*BLOCKSIZE[Y]
                    elif self.direction == DOWN:
                        movement = 0, MAXBMANSPEED
                        position = bomb.getPosition()[X],\
                                   bomb.getPosition()[Y] + 2*BLOCKSIZE[Y]
                    bomb.beingPunched = True
                    bomb.setMovement(movement)
                    bomb.setPosition(position)
                    self.world.flyBomb(bomb)
                self.undoUpdate()

        bombsToSort = self.world.populatedBombGroup.sprites()
        bombsToSort.sort(lambda x, y: cmp(x.id, y.id))
        bombs = spritecollide(self, self.world.bombGroup, 0)
        bombs.sort(lambda x, y: cmp(x.id, y.id))
        for bomb in bombsToSort:
            if(not bomb in bombs):
                population = bomb.getPlaced()
                for bomberguy in population:
                    if (bomberguy.name == self.name):
                        population.remove(bomberguy)
                        break
                bomb.setPlaced(population)
                if(len(bomb.getPlaced()) == 0):
                    self.world.removePopulatedBomb(bomb)
                    break

    def animatePlayer(self):
        """Animate the player's sprite"""
        # Animate players shield or not
        if self.protection > 0:
            dirDict={LEFT :self.left_framesShield,
                 RIGHT:self.right_framesShield,
                 UP   :self.up_framesShield,
                 DOWN :self.down_framesShield}
        else:
            dirDict={LEFT :self.left_frames,
                     RIGHT:self.right_frames,
                     UP   :self.up_frames,
                     DOWN :self.down_frames}

        self.frameIndex = (self.frameIndex + 1) % \
                          (len(dirDict[self.direction]) )
        self.image = dirDict[self.direction][self.frameIndex]

    def faceBomber(self):
        """Alter player's image according to what direction
           he/she is facing
        """
        vector = self.getMovement()
        self.moving = True
        if vector[X] > 0:
            self.direction = RIGHT
        elif vector[X] < 0:
            self.direction = LEFT
        elif vector[Y] > 0:
            self.direction = DOWN
        elif vector[Y] < 0:
            self.direction = UP
        else:
            self.moving = False
            self.frameIndex = 0

    def kill(self):
        # Decrement player lives if they don't have invurnability
        if not self.invulnerability:
            self.player.lives -= 1
            self.player.disableInput()
            Widget.kill(self)
