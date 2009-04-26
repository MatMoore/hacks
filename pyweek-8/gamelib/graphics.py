#TODO

#wrapper for some of the pygame stuff

import data #used for figuring out path of files
import math
import pygame
from pygame.locals import *
from constants import *

class Graphics:
    def __init__(self):
        pygame.init()
        self.images = dict()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.camera = (0,0)
        self.loadImage(BACKGROUNDIMAGE)

    def loadImage(self, fileName):
        if fileName in self.images: #have we already loaded this file
            image = self.images[fileName]
        else:
            image = pygame.image.load(data.filepath('images/'+fileName))
            self.images[fileName] = image
        return image
        
    def clear(self):
        self.screen.fill(FILLCOLOR)

    def flip(self):
        pygame.display.flip()
        
    def calcScreenPos(self, location):
        """given a world location, calculate the position on screen"""
        x = (  location[0] - self.camera[0]  ) + SCREENSIZE[0]/2
        y = (  location[1] - self.camera[1]  ) + SCREENSIZE[1]/2
        return (round(x), round(y))
    
    def calcWorldPos(self, location):
        """given a screen location, calculate the current world location"""
        x = location[0] - SCREENSIZE[0]/2 + self.camera[0]
        y = location[1] - SCREENSIZE[1]/2 + self.camera[1]    
        return (x,y)
        
    def moveCamera(self,dx,dy):
        self.camera = (self.camera[0]+dx,self.camera[1]+dy)

    def drawBackground(self, filename=BACKGROUNDIMAGE):
        """tiles the background image"""
        image = self.loadImage(filename)
        left, top, width, height = image.get_rect()
        xoffset = self.camera[0] % width
        yoffset = self.camera[1] % height
        for x in range(-1, int(math.ceil(SCREENSIZE[0]/width)+2)):
            for y in range(int(math.ceil(SCREENSIZE[1]/height)+2)):
                self.screen.blit(image, (x*width-xoffset, y*height-yoffset))

    def drawImage(self, image, location, angle=0):
        """draw it on the screen if it's visible"""
        if location.__class__ == pygame.rect.Rect:
            worldloc = (location.left, location.top)
        else:
            worldloc = location
        
        size = image.get_rect()
        screenPos = self.calcScreenPos(worldloc)
        
        #make sure it's gonna go on the screen before rotating and blitting it
        if screenPos[0] > 0-size[2] and \
            screenPos[0] < SCREENSIZE[0]+size[2] and \
            screenPos[1] > 0-size[3] and \
            screenPos[1] < SCREENSIZE[1]+size[3]:
            
            if angle <> 0:
                drawImage = pygame.transform.rotozoom(image, 360-angle, 1)
            else:
                drawImage = image
            size = drawImage.get_rect() #because the rotate might have changed it
            loc = (screenPos[0]-size[2]/2, screenPos[1] - size[3]/2)
            self.screen.blit(drawImage, loc)
    
    def drawRect(self, rect, color=DRAGRECTCOLOR, width=2):
        screenrect = (self.calcScreenPos((rect[0],rect[1])), (rect[2], rect[3]))
        pygame.draw.rect(self.screen, color, screenrect, width)
    
    def __del__(self):
        pygame.quit()

