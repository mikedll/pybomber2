import pygame.mixer as sound
from random import *
from pygame.locals import *

# Display
#RESOLUTION = (640,480)
RESOLUTION = (840,600)
FLAGS = HWSURFACE|DOUBLEBUF|ASYNCBLIT
BACKGROUND = 'images/bgd_grass.jpg'
LOCALNAMESFILE = 'localplayernames'
NETWORKNAMESFILE = 'networkplayernames'
HELPURL = 'http://www.cs.ucr.edu/~sbrandon/cs180/'
LOADIMG = 'images/loadscreen.png'

# Game speeds
GAMELOOPTIME = 40
WIDGETFRAMES = 25
MINUTE = 60000 # One minute in ms
# Game values
DEFAULTMAP = 'map/classic.map'
DENSITYMUTABLE = 100
POWERUPCHANCE = 30
GAMETIME = 5*MINUTE # 5 minute game time
                    # For win, must be > BOMBTTL in ms + TIMETOLIVE in ms
GAMETIMEINLOOPS = GAMETIME / GAMELOOPTIME
BOMBTTL = 100
PLACEDTTL = 10 # There is a time for other players to get off placed bomb.
SHORTBOMBTTL = BOMBTTL/3 + 1 # For virus short fuse
REMOTETTL = BOMBTTL*10 # Romote Detonated bombs last longer.
VIRUSTTL = MINUTE/120 # This is 10 seconds
EXPLOSIONTTL = 10
NAPALMTTL = 4
PROTECTIONTTL = 1
TIMETOLIVE = EXPLOSIONTTL + BOMBTTL # Amount of time last remaining player
                                    # must remain alive for in order to win
# Viruses
RUNS = 0
CONFUSION = 1
CONSTIPATION = 2
SHORTFUSE = 3
SHORTRADIUS = 4
TURTLE = 5
VIRUSLIST = [RUNS, CONFUSION, CONSTIPATION, SHORTFUSE, SHORTRADIUS, TURTLE]

# Power-Ups
POWERUPS = {'bombUp': 30,
            'radiusUp': 20,
            'virus': 20,
            'shield': 10,
            'kick': 10,
            'speedUp': 15,
            'napalm': 10,
            'lifeUp': 1,
            'detonateEnable': 5,
            'punch': 10,
            'superSpeedUp': 1,
            'superRadiusUp': 1}
REGULARPOWERUPLIST = 'bombUp', 'kick', 'napalm',\
                     'radiusUp', 'shield', 'speedUp'
SUPERPOWERUPLIST = 'detonateEnable', 'lifeUp', 'superRadiusUp', 'superSpeedUp'

ANIMATEDPOWERUPLIST = 'superRadiusUp', 'superSpeedUp'

WALKOVERCOVERAGE = .60  # Percentage of powerup you have
                        # to cover in order to pick it up

# Map related
MAPLIST = ['map/adam.map',
           'map/bryan.map',
           'map/bullfight.map',
           'map/bunkers.map',
           'map/classic.map',
           'map/compression.map',
           'map/crazy.map',
           'map/dosxx.map',
           'map/football.map',
           'map/longandnarrow.map',
           'map/maze.map',
           'map/moon.map',
           'map/nowheretorun.map',
           'map/oneonone.map',
           'map/original.map',
           'map/punchcaptain.map',
           'map/solid.map',
           'map/stars.map',
           'map/suicide.map',
           'map/suicide2.map',
           'map/sun.map',
           'map/testing.map',
           'map/therug.map',
           'map/volley.map',
           'map/volley2.map']
PLAYERPOS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
POWERUPMAP = {'A': 'radiusUp', 'B': 'bombUp', 'D': 'detonateEnable',
            'E': 'superSpeedUp', 'K': 'kick', 'L': 'lifeUp',
            'N': 'napalm', 'P': 'punch', 'S': 'speedUp', 'V': 'virus',
            'U': 'superRadiusUp'}

# Game sounds
BACKGROUNDMUSICLIST = ['Sounds/soundtrack2.ogg',
                       'Sounds/bgdMusic_short.ogg',
                       'Sounds/Overture1812.ogg'#,
                       #'Sounds/BackgroundMusic/TipsyInst.ogg',
                       #'Sounds/BackgroundMusic/SplashWaterfallsInst.ogg',
                       #'Sounds/BackgroundMusic/DamnInst.ogg'
                      ]
BACKGROUNDMUSIC = 'Sounds/soundtrack2.ogg'
BOMBEXPLOSION = 'Sounds/explosion.ogg'
DROPBOMBSOUND = 'Sounds/bombPlaced.ogg'
BOMBERMANDYING = 'Sounds/playerDies.ogg'
RESPAWN = 'Sounds/respawn1.ogg'
POWERUP = 'Sounds/powerUp.ogg'
SUPERPOWERUP = 'Sounds/superPowerUp.ogg'
VIRUS = 'Sounds/virus.ogg'
VICTORYMUSIC = 'Sounds/soundtrack3.ogg'

# Game World and Map
# How many squares the grid is.
# columns, rows
GAMEWORLDSIZE = 25, 17
COLUMNS = GAMEWORLDSIZE[0]
ROWS = GAMEWORLDSIZE[1]
# Directions are easier to think about this way.
# Just remember (0, 0) is (BOTTOM, LEFT) (like on a graph).
TOP = ROWS - 1
LEFT = 0
RIGHT = COLUMNS - 1
BOTTOM = 0
X = 0
Y = 1

# Widget values
BLOCKSIZE = 32, 32
#if RESOLUTION == (640, 480):
#    BLOCKSIZE = 32, 32
#elif RESOLUTION == (800, 600):
#    BLOCKSIZE = 40, 40
BLOCKCOLORI = 176, 1, 4 # Redish
BLOCKCOLORM = 96, 96, 96 # Gray
PUCE = 104, 28, 35 # Deep red to grayish purple: used for transparency
LAVENDER = 150, 5, 230
# The colors in the colorDict are:
# Red, blue, green, orange, black, white, yellow, light blue, gray, pruple
COLORDICT = {
  0: (255, 0, 0),
  1: (0, 0, 255),
  2: (0, 255, 0),
  3: (255, 127, 0),
  4: (0, 0, 0),
  5: (255, 255, 255),
  6: (255, 255, 0),
  7: (0, 255, 255),
  8: (127, 127, 127),
  9: (255, 0, 255)
}

# Offset
XOFFSET = BLOCKSIZE[0]/2
YOFFSET = BLOCKSIZE[1]/2 + BLOCKSIZE[1]

# Bomberman values
BMANSIZE = 32, 32 # Size of bombers' rect
BMANTURTLE = BMANSIZE[0]/16 # Speed is based on resolition size
BMANSPEED = BMANSIZE[0]/8
MAXBMANSPEED = BMANSIZE[0]/4
# bomber is given about 2 sec of invurnability at the start their life
INVULNERABILITY = 30
STARTCAPACITY = 1
STARTRADIUS = 2
SUPERRADIUS = max(COLUMNS, ROWS)
BMANLIVES = 1
TEXTCOLOR = (255,255,255)
TEXTCOLOR2 = (255,255,100)

# Level of output

DEBUG = 1

# Network section
LISTENTIMEOUT = 30
CONNECTTIMEOUT = 30
STARTGAMEDELAY = 600  # Seconds for clients to wait after they've
                     # connected to the server
HAMMERDELAY = .2     # Pause in seconds in between
                     # accepts()/connects()
PACKETSIZE = 1024
FREEPORT = 35033

QUITCOMMAND = 'qqqq'
STOP = 'ssss'
NOOP = '----'
UP = 'uuuu'
DOWN = 'dddd'
LEFT = 'llll'
RIGHT = 'rrrr'
ACTION = 'aaaa'
BOMB = 'bbbb'
DISCONNECT = 'disc'
COMMANDSET = ([UP, DOWN, LEFT, RIGHT, ACTION, BOMB],
              [DOWN, UP, RIGHT, LEFT, ACTION, BOMB])

NUMCOMMANDSETS = len(COMMANDSET)

# Default Player controls
P1KEYDICT = {
    K_w: UP,
    K_s: DOWN,
    K_a: LEFT,
    K_d: RIGHT,
    K_b: BOMB, K_LSHIFT: BOMB,
    K_n: ACTION, K_LCTRL: ACTION,
    K_ESCAPE: QUITCOMMAND
}

P2KEYDICT = {
    K_UP: UP,
    K_DOWN: DOWN,
    K_LEFT: LEFT,
    K_RIGHT: RIGHT,
    K_KP0: BOMB, K_RCTRL: BOMB,
    K_KP_PERIOD: ACTION, K_RSHIFT: ACTION,
    K_ESCAPE: QUITCOMMAND
}

P3KEYDICT = {
    K_i: UP,
    K_k: DOWN,
    K_j: LEFT,
    K_l: RIGHT,
    K_PERIOD: BOMB,
    K_SLASH: ACTION,
    K_ESCAPE: QUITCOMMAND
}

KEYDICTLIST = P1KEYDICT, P2KEYDICT, P3KEYDICT
ALLKEYS = P1KEYDICT.keys() + P2KEYDICT.keys() + P3KEYDICT.keys()

