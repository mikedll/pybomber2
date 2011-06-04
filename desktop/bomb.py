from widget import *

bomb_image_array = None
napalm_image_array = None
NAPALM_FRAMES = None
BOMB_FRAMES = None

class Bomb(Widget):
    def __init__(self, image, rect, TTL, napalm, radius, name):
        global bomb_image_array, BOMB_FRAMES, napalm_image_array, NAPALM_FRAMES
        if bomb_image_array == None:
             bomb_image_array = pygame.image.load('images/bomb/bomb_strip.png')
             bomb_image_array = pygame.transform.scale(bomb_image_array,\
                                                       (12*32,32))
             try:
                 bomb_image_array = bomb_image_array.convert()
             except:
                 pass
             
             BOMB_FRAMES = createFrames(bomb_image_array)
        if napalm_image_array == None:
            napalm_image_array = pygame.image.load('images/bomb/napalm_strip.png')
            napalm_image_array = pygame.transform.scale(napalm_image_array,\
                                                        (12*32,32))

            try:
                napalm_image_array = napalm_image_array.convert()
            except:
                pass
                                                        
            NAPALM_FRAMES = createFrames(napalm_image_array)
        Widget.__init__(self, image, rect, name)

        self.lastMoved = None
        self.TTL = TTL
        self.napalm = napalm
        self.radius = radius
        self.beingPunched = 0
        self.placed = []
        self.timeDelay = WIDGETFRAMES
        self.last_update = self.timeDelay
        self.frameIndex = 0
        self.modNo = 4
        self.baseFrame = 0
        if self.napalm == 0:
            self.frames = BOMB_FRAMES
        else:
            self.frames = NAPALM_FRAMES
        self.image = self.frames[self.frameIndex]

    def __str__(self):
        return Widget.__str__() + " id=" + str(self.id)

    def tick(self):
        if self.beingPunched == 0:
            self.TTL -= 1

    def readyToExplode(self):
        return self.TTL <= 0

    def getPlaced(self):
        return self.placed

    # For players walking over bombs check
    def setPlaced(self, placedList):
        self.placed = placedList

    def setStop(self):
        """Set movement to 0 and snap to grid."""
        bombsPos = self.getPosition()
        self.setPosition(self.world.snapToGrid(bombsPos))
        self.setMovement([0,0])

    def setTTL(self,TTL):
        self.TTL = TTL

    def update(self):
        """Animate bomb to get madder as TTL decreases"""

        oldIndex = self.frameIndex

        self.frameIndex += 1
        if self.TTL <= 1 * GAMELOOPTIME:
            self.baseFrame = 8
        elif self.TTL <= 2 * GAMELOOPTIME:
            self.baseFrame = 4
        else:
            pass

        self.frameIndex %= self.modNo
        self.frameIndex += self.baseFrame
        self.image = self.frames[self.frameIndex]

        # Redraw this sprite?
        if oldIndex != self.frameIndex or self.getMovement() != [0,0]:
            self.world.dirtyGroup.add(self)

        # Being punched or kicked
        if self.getMovement() != [0,0]:
            self.lastRect = Rect(self.rect)
            self.rect.move_ip(self.movement)

            # Handle punch
            if self.beingPunched:
                self.world.worldWrap(self)
                objectOnGround = spritecollideany(self, self.world.groundGroup)
                if objectOnGround == None:
                    self.setStop()
                    self.beingPunched = False
                    self.world.groundBomb(self)
            # Handle kick in opposite manner
            else:
                objectsOnGround = spritecollide(self,
                                                self.world.groundGroup,
                                                0)
                if len(objectsOnGround) > 1:
                    self.undoUpdate()
                    self.setStop()
