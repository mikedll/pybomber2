from widget import *

super_radius_up_array = None
speed_image_array = None
S_RADIUS_FRAMES = None
S_SPEED_FRAMES = None

class PowerUp(Widget):
    def __init__(self, rect, kind):
        self.image = pygame.image.load('images/power_' + kind + '.png')
        global super_radius_up_array, speed_image_array,\
               S_RADIUS_FRAMES, S_SPEED_FRAMES

        if super_radius_up_array == None:
            super_radius_up_array = pygame.image.load\
                                    ('images/superRadiusUp/super_radius_up_strip.png')
            super_radius_up_array = pygame.transform.scale\
                                    (super_radius_up_array, (6*32,32))
            try:
                super_radius_up_array = super_radius_up_array.convert()
            except:
                pass
            S_RADIUS_FRAMES = createFrames(super_radius_up_array)

        if speed_image_array == None:
            speed_image_array = pygame.image.load('images/superSpeedUp_strip.png')
            try:
                speed_image_array = speed_image_array.convert()
            except:
                pass
            S_SPEED_FRAMES = createFrames(speed_image_array)

        Widget.__init__(self, self.image, rect)
        self.kind = kind

        try:
            self.image = self.image.convert()
        except:
            pass
        self.image.set_colorkey(PUCE, RLEACCEL)

        if (self.kind == 'superRadiusUp'):
            self.startAnimation( S_RADIUS_FRAMES, 0, 10)

        elif (self.kind == 'superSpeedUp'):
            self.startAnimation( S_SPEED_FRAMES, 0, 15)

    def __str__(self):
        return str(self.id)

    def activate(self, bomber, virus):
        #play super power-up sound
        if self.kind in SUPERPOWERUPLIST:
            self.superPowerUpSound()
            
        #play regular power-up sound
        else:
            self.powerUpSound()

        # Virus
        if self.kind == 'virus':
            # Activate a random virus....
            # Play virus pick up sound
            self.virusSound()
            bomber.virusDict[virus] = VIRUSTTL
            # Special case for Confusion
            if virus == CONFUSION:
                bomber.player.commandSet = COMMANDSET[1]
                
        # BombUp
        elif self.kind == 'bombUp':
            bomber.capacity += 1

        # DetonateEnable
        elif self.kind == 'detonateEnable':
            bomber.detonateEnable = True
            bomber.TTL = REMOTETTL
            bomber.punch = False

        # Kick
        elif self.kind == 'kick':
            bomber.kick = True

        # LifeUp
        elif self.kind == 'lifeUp':
            bomber.player.lives += 1

        # Napalm
        elif self.kind == 'napalm':
            bomber.napalm += NAPALMTTL

        # Punch
        elif self.kind == 'punch':
            bomber.punch = True
            bomber.TTL = BOMBTTL
            bomber.detonateEnable = False

        # RadiusUp
        elif self.kind == 'radiusUp':
            bomber.radius += 1
            
        # Shield
        elif self.kind == 'shield':
            bomber.protection += PROTECTIONTTL
            # Force shield animation
            bomber.last_update -= self.timeDelay
            bomber.animatePlayer()

        # SpeedUp
        elif self.kind == 'speedUp' and bomber.speed < MAXBMANSPEED:
            bomber.speed += 1

        # SuperRadiusUp
        elif self.kind == 'superRadiusUp':
            bomber.radius = SUPERRADIUS

        # superSpeedUp
        elif self.kind == 'superSpeedUp':
            bomber.speed = MAXBMANSPEED
        else:
            print 'Unknown power-up!'

    def attachToWorld(self, world):
        self.world = world
        self.id = self.world.curWidgetID
        self.world.curWidgetID += 1
        debug(str(self.kind) + "\n")

    # For Event Sounds
    def powerUpSound(self):
        try:
            PS = sound.Sound(POWERUP)
            PS.set_volume(0.4)
            PS.play(0)
        except:
            pass

    def superPowerUpSound(self):
        try:
            SP = sound.Sound(SUPERPOWERUP)
            SP.play(0)
        except:
            pass

    def virusSound(self):
        try:
            VS = sound.Sound(VIRUS)
            VS.play(0)
        except:
            pass

    def update(self):
        Widget.update(self)
        # Animated power-ups are always dirty
        if self.kind in ANIMATEDPOWERUPLIST:
            self.world.dirtyGroup.add(self)

