import pygame
from pygame.locals import *
import graphics
import world
import player
import mapobject
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
        self.human = player.Player()
        for i in range(3):
            unit = self.human.buyUnit("SoldierUnit",self.graphics)
            if unit:
                self.world.addUnit(unit)
        unit = self.human.buyUnit("WorkerUnit",self.graphics)
        self.world.addUnit(unit)
        #self.AIPlayers = [player.Player()] #ai does nothing yet
        #for i in range(3):
        #    unit = self.AIPlayers[0].buyUnit("Unit",self.graphics)
        #    if unit:
        #        self.world.addUnit(unit)
            
        self.world.addResource(mapobject.Leaves((100,100),self.graphics)) #this should probably go in world but it needs graphics garghghah

        self.world.addObject(mapobject.Colony((-200,0),self.graphics)) #this should probably go in world but it needs graphics garghghah
        self.input = Input()
        self.input.onClick(self.leftClick)
        self.input.onRightClick(self.rightClick)
        self.input.onDrag(self.drag)

        #make gui
        self.gui = graphics.ContainerWidget()
        self.gui.add(graphics.ResourceDisplay(self.human))
        buildWidget = graphics.BuildWidget(pygame.Rect((0,0),(130,300)),(200,200,200))
        buildWidget.add(graphics.Button(pygame.Rect((0,0),(50,50)),'Soldier',bgColor=(100,100,100),action=self.buySoldier))
        buildWidget.add(graphics.Button(pygame.Rect((0,0),(50,50)),'Worker',bgColor=(100,100,100),action=self.buyWorker))
        buildWidget.add(graphics.Button(pygame.Rect((0,0),(50,50)),'Queen',bgColor=(100,100,100)))
        self.gui.add(buildWidget)
    
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
        unit = self.human.buyUnit("SoldierUnit",self.graphics)
        if unit:
            self.world.addUnit(unit)

    def buyWorker(self):
        unit = self.human.buyUnit("WorkerUnit",self.graphics)
        if unit:
            self.world.addUnit(unit)

    def doScroll(self, dt):
        x, y = pygame.mouse.get_pos()
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
                            
            self.world.update(dt)
            self.world.draw(self.graphics)
            if self.input.dragRect != None:
                self.graphics.drawRect(self.input.dragRect)
            self.human.drawSelectedRects(self.graphics)
            self.gui.draw(self.graphics)
            self.graphics.flip()

if __name__ == '__main__':
    game = maingame()
    game.run()
