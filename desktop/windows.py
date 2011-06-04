"""Code to create text and buttons on the screen """

import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.font import Font
from config import TEXTCOLOR, TEXTCOLOR2


class TextBar(Sprite):
    def __init__(self, text, rect, fontSize):
        Sprite.__init__(self)
        self.font = Font(None, fontSize)
        self.rect = Rect(rect)
        self.image = pygame.surface.Surface((rect[2],
                                             rect[3]))
        self.image = self.font.render(text, 0, TEXTCOLOR)
    def setText(self, text):
        self.image = self.font.render(text, 0, TEXTCOLOR)


class TextInput(Sprite):
    """
    >>> import pygame
    >>> from color_picker import *
    >>> pygame.font.init()

    Set text
    >>> text = "Hello World!"
    >>> testRect = Rect((0,0),(20,20))
    >>> theInput = TextInput(text, testRect)
    >>> theInput.getText()
    'Hello World!'

    Add a character to a string
    >>> theInput.appendChar(103)
    >>> theInput.getText()
    'Hello World!g'

    Delete a character from a string
    >>> theInput.deleteChar()
    >>> theInput.getText()
    'Hello World!'
    """

    def __init__(self, text, rect, fontSize):
        Sprite.__init__(self)
        self.font = Font(None, fontSize)
        self.text = text
        self.rect = Rect(rect)
        self.image = self.font.render(text, 0, TEXTCOLOR2)

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text
        self.image = self.font.render(self.text, 0, TEXTCOLOR2)

    def appendChar(self, char):
        self.text = self.text + chr(char)
        self.image = self.font.render(self.text, 0, TEXTCOLOR2)
        
    def deleteChar(self):
        self.text = self.text[0:-1]
        self.image = self.font.render(self.text, 0, TEXTCOLOR2)

