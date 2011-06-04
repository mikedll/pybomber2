from pygame import display as Display
from pygame.surface import Surface
from pygame.sprite import RenderUpdates as SpriteGroup
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.font import Font
from config import *
import pygame
import time as t
from widget import *
from windows import TextBar

def getEndGameSplash(winnerName = None, winnerColor = None):
    """If winningName and winnerColor are both None,
       display a tie game screen.
    """

    screen = Display.get_surface()
    splashGroup = SpriteGroup()
    if(winnerName != None and winnerColor != None):
        # Create winning bomberman image
        fatalityRect = Rect((0, 0, 500, 500))
        fatalityRect.centerx = screen.get_rect().centerx
        fatalityRect.centery = screen.get_rect().centery
        fatalityAnimation = WorldlessWidget(Surface((500, 500)), fatalityRect)
        fatalImage = pygame.image.load('images/fatality.png').convert()
        fatalImage.set_colorkey(LAVENDER)
        bmanColor = Surface((fatalImage.get_width(),
                          fatalImage.get_height()))
        bmanColor.fill(winnerColor)
        bmanColor.blit(fatalImage, bmanColor.get_rect())
        winnerFrames = createFrames(bmanColor)
        fatalityAnimation.startAnimation(winnerFrames, 0, 12)
        splashGroup.add(fatalityAnimation)

        # Create text for winning player
        winnerText = TextBar(winnerName + \
                             ' Wins!', (0, 0, 200, 50), 50)
        imgWidth = winnerText.image.get_width()
        winnerText.rect.left = (screen.get_size()[X]-imgWidth)/2
        splashGroup.add(winnerText)
    else:
        tieText = TextBar('TIE GAME!',
                                 (0, 20, 250, 50), 35)
        imgWidth = tieText.image.get_width()
        tieText.rect.left = (screen.get_size()[X]-imgWidth)/2
        splashGroup.add(tieText)

    escMessage = TextBar("Press Escape to exit.", (0, 60, 250, 50), 25)
    imgWidth = escMessage.image.get_width()
    escMessage.rect.left = (screen.get_size()[X] - imgWidth) / 2
    splashGroup.add(escMessage)

    pressKeyText = TextBar('Press a key or button when ready. Next round will start when everyone is ready.',
                           (0, 90, 250, 50), 25)
    imgWidth = pressKeyText.image.get_width()
    pressKeyText.rect.left = (screen.get_size()[X] - imgWidth) / 2
    splashGroup.add(pressKeyText)

    return splashGroup

def getLoadScreen():
    screen = Display.get_surface()
    splashGroup = SpriteGroup()

    # Create text for connecting player
    connectingText = TextBar ('Loading...', (0, 20, 250, 50), 35)
    imgWidth = connectingText.image.get_width()
    connectingText.rect.left = (screen.get_size()[X] - imgWidth) / 2
    splashGroup.add(connectingText)

    return splashGroup,connectingText

