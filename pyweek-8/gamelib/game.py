import pygame
from pygame.locals import *
import graphics
import world
import player
import mapobject
import random
import math
import aiplayer
from constants import *

class Input:
    '''Reusable input class for handling mouse and keyboard input.'''
    def __init__(self):
        self.clickLoc = None
        self.dragRect = None

        #functions to call for these things
        self.click = None
        self.drag = None
        self.keyPress = {}
        self.rightClick = None

    def onClick(self,f):
        self.click = f

    def onKeypress(self,key,f):
        self.keyPress[key] = f
        
    def onRightClick(self,f):
        self.rightClick = f

    def onDrag(self,f):
        self.drag = f

    def doInputEvents(self,graphics):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
            if event.type == MOUSEBUTTONDOWN:
                self.clickLoc = graphics.calcWorldPos(pygame.mouse.get_pos())
            
            if event.type == MOUSEBUTTONUP:
                if self.dragRect == None:
                    if event.button == 1 and self.clickLoc: #left click
                        self.click(self.clickLoc)
                    elif event.button == 3 and self.clickLoc: #right click
                        self.rightClick(self.clickLoc)
                        
                else:
                    if event.button == 1 and self.dragRect: #left drag
                        self.drag(self.dragRect)
                self.clickLoc = None
                self.dragRect = None
        
        
        #This bit makes the drag rectangle
        if self.clickLoc != None:   #if we're clicking
            loc = graphics.calcWorldPos(pygame.mouse.get_pos())
            #check if we've moved more than DRAGDISTANCE pixels in either direction
            if (self.dragRect != None) or (abs(self.clickLoc[0] - loc[0]) > DRAGDISTANCE) or (abs(self.clickLoc[1] - loc[1]) > DRAGDISTANCE):
                self.dragRect = pygame.Rect(self.clickLoc[0],self.clickLoc[1],loc[0]-self.clickLoc[0], loc[1]-self.clickLoc[1])

        return True
    

class Game:
    def __init__(self):
        self.graphics = graphics.Graphics()
        self.world = world.World()
        self.state = GAMESTATE_RUN

        #create human player
        self.human = player.Player(self.graphics, self.world,team=1)
        position = (0,0)
        colony = mapobject.Colony(self.human,position,self.graphics)
        self.world.addObject(colony)
        self.human.addColony(colony)
        
        #create AI Player
        self.AIPlayer = aiplayer.AIPlayer(self.graphics, self.world,team=2) #ai does nothing yet
        #generate random position for AI colony
        randomAngle = random.randint(0,360)
        randomDist = math.sqrt(random.random()*((MAXAIDISTANCE-MINAIDISTANCE)**2) ) + MINAIDISTANCE #this ensures that the random targets are uniformly spread out over the sector
        position = (position[0]+randomDist*math.cos(randomAngle*math.pi/180),position[1]+randomDist*math.sin(randomAngle*math.pi/180))
        
        colony = mapobject.Colony(self.AIPlayer,position,self.graphics,team=2)
        print "AI position: " + str(position)
        self.world.addObject(colony)
        self.AIPlayer.addColony(colony)
    
        self.world.addLeaves(self.graphics)  #add lots of random leaves
        
        self.input = Input()
        self.input.onClick(self.leftClick)
        self.input.onRightClick(self.rightClick)
        self.input.onDrag(self.drag)

        #make gui
        self.gui = graphics.ContainerWidget()
        self.gui.add(graphics.ResourceDisplay(self.human))
        workerImage= self.graphics.loadImage('workerbutton.png')
        soldierImage= self.graphics.loadImage('soldierbutton.png')
        buildWidget = graphics.BuildWidget(pygame.Rect((0,0),(116,61)),(200,200,200))
        buildWidget.add(graphics.Button(pygame.Rect((0,0),(50,50)),image=soldierImage,bgColor=(100,100,100),action=self.buySoldier))
        buildWidget.add(graphics.Button(pygame.Rect((0,0),(50,50)),image=workerImage,bgColor=(100,100,100),action=self.buyWorker))
        self.gui.add(buildWidget)
        position = self.graphics.normalizeScreenCoords((-150,-150))
        rect = pygame.Rect(position,(150,150))
        minimap = graphics.Minimap(rect,self.world,self.graphics)
        self.gui.add(minimap)
    
    def drag(self,dragRect):
        self.human.doSelect(dragRect)

    def leftClick(self,pos):
        screenPos = self.graphics.calcScreenPos(pos)
        if not self.gui.click(screenPos): #can't click on GUI
            self.human.doSelect(pos) 

    def rightClick(self,pos):
        screenPos = self.graphics.calcScreenPos(pos)
        if not self.gui.click(screenPos): #can't click on GUI
            target = self.world.getUnit(pos)
            resource = self.world.getResource(pos)
            if target and (self.human.isUnit(target) == False):
                self.human.doAttack(target)
            elif resource:
                self.human.doGather(resource)
            else:
                self.human.doMove(pos)

    def buySoldier(self):
        unit = self.human.buyUnit("SoldierUnit")

    def buyWorker(self):
        unit = self.human.buyUnit("WorkerUnit")


    def doScroll(self, dt):
        x, y = pygame.mouse.get_pos()
        if self.gui.mouseOver((x,y)):
            return
        dx,dy = (0,0)
        if x < SCROLLWIDTH:
            dx = - SCROLLSPEED*dt
        elif x > (SCREENSIZE[0]-SCROLLWIDTH):
            dx = SCROLLSPEED*dt
        if y < SCROLLWIDTH:
            dy = -SCROLLSPEED*dt
        elif y > (SCREENSIZE[1]-SCROLLWIDTH):
            dy = SCROLLSPEED*dt
        if dx or dy:
            self.graphics.moveCamera(dx,dy)
    
    def run(self):
        newtime = pygame.time.get_ticks()
        while self.state == GAMESTATE_RUN:
            oldtime = newtime
            newtime = pygame.time.get_ticks()
            dt = (newtime - oldtime)/1000.0

            self.doScroll(dt)
            
            if self.input.doInputEvents(self.graphics) == False:
                self.state = GAMESTATE_QUIT

            buildStatus = self.human.getBuildStatus()   #this simultaneously updates the build status and returns whether it's built or not
            if buildStatus != None:
                #print buildStatus
                pass    #TODO: display some progress bar here
            self.AIPlayer.update()
            self.world.update(dt)
            self.world.draw(self.graphics)
            if self.input.dragRect != None:
                self.graphics.drawRect(self.input.dragRect)
            self.human.drawSelectedRects()
            self.gui.draw(self.graphics)
#            self.world.drawMinimap(self.graphics)
            self.graphics.flip()

if __name__ == '__main__':
    game = maingame()
    game.run()
