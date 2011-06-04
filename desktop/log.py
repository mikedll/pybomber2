from socket import gethostname
from config import RESOLUTION, LOADIMG
import pygame.display as Display
from pygame.surface import Surface
import pygame.image

# For coordinating loading screens
curGroup = None
screen = None
curTextBar = None
logfile = None

def updateLoadScreen(message):
    global screen, curTextBar, curGroup, background
    if(screen == None):
        return
    screen = Display.get_surface()
    curGroup.clear(screen, background)

    # Updated text
    curTextBar.setText(message)
    curTextBar.rect.centerx = screen.get_rect().centerx
    
    curGroup.draw(screen)
    Display.flip()

def initLoadScreen(group, textBar):
    global curGroup, screen, curTextBar, background
    screen = Display.get_surface()
    background = pygame.image.load(LOADIMG)
    screen.blit(background, background.get_rect())
    curGroup = group
    curTextBar = textBar
    curGroup.draw(screen)
    Display.flip()
    

def initDebugLog():
    global logfile
    logfile = file("actions.log"+gethostname(), "w")
    

def debug(info):
    global logfile
    if logfile != None:
        logfile.write(str(info) + "\n")

