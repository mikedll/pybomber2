#!/usr/bin/python2.3 -tt
""" This is a tester to view animations
    Usage: >animviewer.py image_file fps
"""
import sys
try:
    import pygame
except:
    print "Install pygame."
    sys.exit()
from pygame.sprite import RenderUpdates as SpriteGroup
from config import PUCE
from widget import *
import time as t

pygame.display.init()

class Animation(Widget):
    def __init__(self, surface, rect, array):
        Widget.__init__(self, surface, rect)
        try:
            self.image_array = pygame.image.load(array).convert()
        except:
            self.image_array = pygame.image.load(array)

        self.frameNo = 0
        self.frames = self.createFrames(self.image_array)
        self.image = self.frames[self.frameNo]

    def update(self):
        self.frameNo = ((self.frameNo+1)%(len(self.frames)))
        self.image = self.frames[self.frameNo]

    def createFrames(self, image):
        fr_width = image.get_height()
        fr_size = fr_width, fr_width
        frames = []
        for frame_no in range(0, image.get_width(), fr_width):
            frame = pygame.Surface(fr_size)
            frame.blit(image, (0,0), ((frame_no,0), fr_size))
            frame.set_colorkey(PUCE, RLEACCEL)
            frames.append(frame)
        return frames


def main():
    # Get filename
    try:
        image_file = sys.argv[1]
        framerate = sys.argv[2]
    except:
        image_file = raw_input("Enter name of image file: ")
        framerate = raw_input("Enter framerate: ")

    timedelay = (1.0)/(float(framerate))
    # Initialize display
    try:
        screen = pygame.display.set_mode((600,600),
                                    HWSURFACE|DOUBLEBUF)
    except:
        screen = pygame.display.set_mode((600,600))

    background = pygame.image.load(BACKGROUND).convert()
    screen.blit(background, (0,0,400,400))

    temp_img = pygame.image.load(image_file)
    anim_size = (temp_img.get_height(), temp_img.get_height())
    surf = pygame.surface.Surface(anim_size)
    anim = Animation(surf, (0,0,temp_img.get_height(),temp_img.get_height()),
                     image_file)
    sprites = SpriteGroup()
    sprites.add(anim)

    # Display animation
    pygame.display.flip()

    while 1:
        cur_time = t.time()
        sprites.clear(screen, background)
        sprites.update()
        dirty = sprites.draw(screen)
        pygame.display.update(dirty)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

        t.sleep(t.time() - cur_time + timedelay)

if __name__ == "__main__":
    main()
