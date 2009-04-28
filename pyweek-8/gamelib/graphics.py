#TODO

#wrapper for some of the pygame stuff

import data #used for figuring out path of files
import math
import pygame
from pygame.locals import *
from constants import *

class Widget:
    '''Something that remains fixed in screen coordinates'''
    def __init__(self):
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self,graphics):
        pass

    def click(self,position):
        pass

    def mouseOver(self,position):
        pass


class Button(Widget):
    '''Clickable buttons'''
    def __init__(self,rect,text,bgColor=None,image=None,mouseOverImage=None,action=None):
        pass

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self,graphics):
        pass

    def click(self,position):
        pass

class GUI(Widget):
    '''All GUI components'''
    def __init__(self):
        Widget.__init__(self) 
        self.components = []

    def add(self,widget):
        self.components.append(widget)

    def draw(self,graphics):
        if self.visible:
            for i in self.components:
                i.draw(graphics)

class ResourceDisplay(Widget):
    '''Show the amount of leaves the player has'''
    def __init__(self,player):
        self.player = player

    def draw(self,graphics):
        text=str(self.player.leaves)
        width=graphics.font.size(text)[0] 
        graphics.writeText(text,(-5-width,5)) #should probably make this function support right alignement instead of doing it here

class BuildWidget(Widget):
    '''Collection of buttons (for building new units)'''
    def __init__(self,rect,bgcolor=None):
        self.buttons=[]
        self.rect = rect
        left = self.rect.left+BUTTONSPACING
        top = self.rect.top+BUTTONSPACING
        right = self.rect.right-BUTTONSPACING
        bottom = self.rect.bottom-BUTTONSPACING
        self.x=left #x position of the current column
        self.y=top #y position of the current row
        self.nextline = top #y position of the next row

    def show(self):
        for i in self.buttons:
            i.show()

    def hide(self):
        for i in self.buttons:
            i.hide()

    def draw(self,graphics):
        '''Draw all the buttons in a nice box'''
        for i in self.buttons:
            i.draw(graphics)

    def add(self,button):
        '''Align a new button inside the box'''
        if x+button.rect.width < right: #fits horizontally
            if y+button.rect.height < bottom: #fits vertically
                button.topleft = (x,y) #move to the right of the previous one
                self.buttons.append(button)
        elif y+button.rect.height < bottom: #move onto the next line
            self.y=self.nextline
            self.x=self.rect.left+BUTTONSPACING
            button.topleft = (x,y)
            self.buttons.append(button)
        else:
            return False #no room for additional buttons :o
        
        #work out position for the next button
        self.x += button.width + BUTTONSPACING #position for next button to the right
        if self.y+button.height+BUTTONSPACING > self.nextline:
            self.nextline = self.y+button.height+BUTTONSPACING #position for the next line below this one
        return True

class Graphics:
    def __init__(self):
        pygame.init()
        self.images = dict()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.camera = (0,0)
        self.loadImage(BACKGROUNDIMAGE)
        font = pygame.font.get_default_font()
        self.font = pygame.font.Font(font,24) #TODO: make this more flexible (e.g. support multiple sizes), bundle a prettier font

    def normalizeScreenCoords(self,pos):
        x,y=pos
        if x < 0:
            x += self.screen.get_width()
        if y < 0:
            y += self.screen.get_height()
        return (x,y)

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

    def writeText(self,text,position,color=(0,0,0),bgcolor=None,center=False):
        '''Write text to screen. If center is true text will be centered at position, else position is taken to be the top left corner. Position in screen coordinates.'''
        text=self.font.render(text,True,color)
        if center:
            position = (position[0]-text.width/2,position[1]-text.height/2)
        self.drawStaticImage(text,position)

    def drawStaticImage(self,image,location,angle=0):
        '''Draw an image on the screen. Location is the top left in screen coordinates.'''
        location = self.normalizeScreenCoords(location) #accept negative values
        self.screen.blit(image, location)

    def drawImage(self, image, location, angle=0):
        """Draw an image on the screen if it's visible (screen position changes if the camera moves). Location is in world coordinates."""
        if location.__class__ == pygame.rect.Rect:
            worldLoc = location.center
        else:
            worldLoc = location

        size = image.get_size()
        #make sure it's gonna go on the screen before rotating and blitting it
        screenPos = self.calcScreenPos(worldLoc)
        if screenPos[0] > 0-size[0] and \
            screenPos[0] < SCREENSIZE[0]+size[0] and \
            screenPos[1] > 0-size[1] and \
            screenPos[1] < SCREENSIZE[1]+size[1]:
            
            if angle <> 0:
                drawImage = pygame.transform.rotozoom(image, 360-angle, 1)
            else:
                drawImage = image
            rect = drawImage.get_rect() #because the rotate might have changed it
            rect.center = worldLoc      #set the center back to where we were, cause this can change with rotation
            loc = self.calcScreenPos((rect.left, rect.top))     #get the screen pos for the top left(after rotation)
            self.screen.blit(drawImage, loc)
            return rect
        return location
        
    def drawRect(self, rect, color=DRAGRECTCOLOR, width=2):
        screenrect = (self.calcScreenPos((rect[0],rect[1])), (rect[2], rect[3]))
        pygame.draw.rect(self.screen, color, screenrect, width)
    
    def __del__(self):
        pygame.quit()

