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
        '''What happens if it is clicked. Return value is True if position collides with the widget, False otherwise'''
        return False

    def mouseOver(self,position):
        '''What happens on mouseover. Return value is True if position collides with the widget, False otherwise'''
        return False

class ContainerWidget(Widget):
    '''Widget which contains more widgets'''
    def __init__(self):
        Widget.__init__(self) 
        self.components = []

    def add(self,widget):
        self.components.append(widget)

    def show(self):
        for i in self.components:
            i.show()

    def hide(self):
        for i in self.components:
            i.hide()

    def draw(self,graphics):
        if self.visible:
            for i in self.components:
                i.draw(graphics)

    def click(self,position):
        '''Attempt to click on a component. Returns true if successful'''
        for i in self.components:
            if i.click(position):
                return True
        return False

class Button(Widget):
    '''Clickable buttons'''
    def __init__(self,rect,text,color=None,bgColor=None,image=None,mouseOverImage=None,action=None):
        Widget.__init__(self)
        self.rect = rect
        self.action = action
        self.bgColor = bgColor
        self.image = image
        self.text = text

    def draw(self,graphics):
        if self.visible:
            if self.image:
                graphics.drawStaticImage(self.image,self.rect.topleft)
            elif self.bgColor:
                graphics.drawStaticRect(self.rect, self.bgColor, 0)
            graphics.writeText(self.text,self.rect.center,center=True,rect=self.rect)

    def click(self,position):
        if self.rect.collidepoint(position):
            if self.action:
                self.action()
            return True
        else:
            return False

class ResourceDisplay(Widget):
    '''Show the amount of leaves the player has'''
    def __init__(self,player):
        self.player = player

    def draw(self,graphics):
        text=str(self.player.leaves)
        width=graphics.font.size(text)[0] 
        position = graphics.normalizeScreenCoords((-5-width,5))
        graphics.writeText(text,position) #should probably make this function support right alignement instead of doing it here

class BuildWidget(ContainerWidget):
    '''Collection of buttons (for building new units)'''
    def __init__(self,rect,bgcolor=None):
        ContainerWidget.__init__(self)
        self.bgColor = bgcolor
        self.rect = rect
        left = self.rect.left+BUTTONSPACING
        top = self.rect.top+BUTTONSPACING
        right = self.rect.right-BUTTONSPACING
        bottom = self.rect.bottom-BUTTONSPACING
        self.x=left #x position of the current column
        self.y=top #y position of the current row
        self.nextline = top #y position of the next row

    
    def draw(self,graphics):
        '''Draw all the buttons in a nice box'''
        if self.visible:
            #draw background
            if self.bgColor:
                graphics.drawStaticRect(self.rect, color=self.bgColor, width=0)

            #draw buttons
            for i in self.components:
                i.draw(graphics)

    def add(self,button):
        '''Align a new button inside the box'''
        if self.x+button.rect.width < self.rect.right-BUTTONSPACING: #fits horizontally
            if self.y+button.rect.height < self.rect.bottom-BUTTONSPACING: #fits vertically
                button.rect.topleft = (self.x,self.y) #move to the right of the previous one
                self.components.append(button)
        elif self.y+button.rect.height < self.rect.bottom-BUTTONSPACING: #move onto the next line
            self.y=self.nextline
            self.x=self.rect.left+BUTTONSPACING
            button.rect.topleft = (self.x,self.y)
            self.components.append(button)
        else:
            return False #no room for additional buttons :o
        
        #work out position for the next button
        self.x += button.rect.width + BUTTONSPACING #position for next button to the right
        if self.y+button.rect.height+BUTTONSPACING > self.nextline:
            self.nextline = self.y+button.rect.height+BUTTONSPACING #position for the next line below this one
        return True

    def click(self,pos):
        '''Attempt to click on the widget. Returns false if pos is outside the widget'''
        if self.rect.collidepoint(pos):
            #check to see if one of the buttons was clicked
            for i in self.components:
                if i.click(pos):
                    break
            return True
        else:
            return False

class Graphics:
    def __init__(self):
        pygame.init()
        self.images = dict()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.camera = (0,0)
        self.loadImage(BACKGROUNDIMAGE)
        font = pygame.font.get_default_font()
        self.font = pygame.font.Font(font,14) #TODO: make this more flexible (e.g. support multiple sizes), bundle a prettier font

    def normalizeScreenCoords(self,pos):
        x,y=pos
        if x < 0:
            x += self.screen.get_width()
        if y < 0:
            y += self.screen.get_height()
        return (x,y)

    def getCameraRect(self):
        rect = pygame.Rect((0,0),self.screen.get_size())
        rect.center = self.camera
        return rect

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

    def writeText(self,text,position,color=(0,0,0),bgcolor=None,center=False,rect=None):
        '''Write text to screen. If rect is specified then it will be cropped to the rect. If center is true text will be centered at position, else position is taken to be the top left corner. Position in screen coordinates.'''
        text=self.font.render(text,True,color)
        if center:
            position = (position[0]-text.get_width()/2,position[1]-text.get_height()/2)
        if rect:
            #find the portion of the textbox which is in this rect
            textBox = pygame.Rect(position,text.get_size())
            rect2 = textBox.clip(rect)
            position = rect2.topleft
            rect2.top -= textBox.top #need rect coordinates relative to the textbox for the blit
            rect2.left -= textBox.left
            self.drawStaticImage(text,position,rect=rect2)
            
        else:
            self.drawStaticImage(text,position)

    def drawStaticImage(self,image,location,angle=0,rect=None):
        '''Draw an image on the screen. Location is the top left in screen coordinates. '''
        #location = self.normalizeScreenCoords(location) #accept negative values          
        self.screen.blit(image, location, rect)
        
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
            
            if angle != 270 and angle != -90:
                drawImage = pygame.transform.rotozoom(image, 270-angle, 1)
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
        self.drawStaticRect(screenrect, color, width)

    def drawLine(self, p1, p2, color=LASERCOLOR, width=4):
        p1 = self.calcScreenPos(p1)
        p2 = self.calcScreenPos(p2)
        pygame.draw.line(self.screen, color, p1, p2, width)

    def drawStaticRect(self,screenrect,color=DRAGRECTCOLOR, width=2):
        pygame.draw.rect(self.screen, color, screenrect, width)

    def drawStaticCircle(self,center,radius,color=DRAGRECTCOLOR, width=2):
        pygame.draw.circle(self.screen, color, center, radius, width)
    
    def __del__(self):
        pygame.quit()

