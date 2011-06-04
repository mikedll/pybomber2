import pygame
from pygame.locals import *


class Translator:
    def __init__(self):
        self.count = pygame.joystick.get_count()
        self.array = []
        if self.count == 0:
            return
        for pad in range(self.count):
            self.array.append(pygame.joystick.Joystick(pad))
            self.array[pad].init()
        return

    def joyEnabled(self, name):
        for pad in self.array:
            if name == str(pad.get_id()):
                pad.init()
                return pad
        return None

