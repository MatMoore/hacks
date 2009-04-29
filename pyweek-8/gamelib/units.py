#TODO

#all units inherit from a basic unit class, which inherits from mapobject

#have some basic stats
#and a state (what they are currently doing)

#need an interact method which takes a list of visible stuff, and the unit changes its state as appropriate

import math
import pygame
import animation
import mapobject
import stuff
from constants import *

#not sure if this is right so it's not being used for now
def circleLineIntersect(c, radius, p1, p2):
    direction = (p2[0] - p1[0], p2[0] - p1[0])
    diff = (c[1] - p1[1], c[1] - p1[1])
    t = float(diff[0]*direction[0]+diff[1]*direction[1]) / float(direction[0]*direction[0]+direction[1]*direction[1])
    if (t < 0):
        t = 0
    elif (t > 1):
        t = 1
    closest = ((p1[0] + t * direction[0]),(p1[1] + t * direction[1]))
    d = (c[0] - closest[0],c[1] - closest[1])
    distsqr = d[0]*d[0]+d[1]*d[1]
    collides = (distsqr <= (radius * radius))
    return collides
    


    
class Unit(mapobject.MapObject):
    """Base class for units (anything which can move)"""
    price = 0

    def __init__(self, graphics, position, animations):
        self.position = position
        self.health = 100
        self.maxHealth = 100
        self.speed = 25
        self.targets = [] #walk target
        self.gatherTarget = pygame.sprite.Group()   #i've kept these here so that the collision avoidance can check
        self.attackTarget = pygame.sprite.Group()   #whether this unit is just trying to move or whether it's doing
                                                    #something useful - maybe there's a better way


        self.animations = dict()
        for action,anim in animations.iteritems():
            self.animations[action] = animation.Animation(graphics, anim)
        
        self.currentanimation = self.animations['default']  #set us to the default animation
        mapobject.MapObject.__init__(self, self.currentanimation.reset(), position) #init the base class with the first frame of the animation
        self.direction = 100
        
    def getDistance(self, target):
        """get the distance from current location to target"""
        return math.sqrt(float((target[0]-self.position[0])**2+(target[1]-self.position[1])**2))

    def getAngleTo(self, target):
        result = math.atan2(target[1]-self.position[1], target[0]-self.position[0])*180/math.pi + 90
        if result < 0:
            result += 360
        return result
        
    def isDead(self):
        return self.health <= 0

    def update(self,dt):
        #continue animation    
        self.surface = self.currentanimation.update(dt)


        #keep moving if walking towards something
        if len(self.targets) > 0:
            target = self.targets[-1]
        
            #calculate desired heading
            desiredDirection = self.getAngleTo(target)
                
            #now correct for the discontinuity(360 == 0) so we can turn left or right correctly
            while abs(self.direction - desiredDirection) > 180:
                if self.direction < desiredDirection:
                    desiredDirection -= 360
                elif self.direction > desiredDirection:
                    desiredDirection += 360

            if desiredDirection < self.direction:
                self.direction -= TURNSPEED * dt    #turn left
            elif desiredDirection > self.direction:
                self.direction += TURNSPEED * dt    #turn right
            
            if abs(self.direction - desiredDirection) < TURNSPEED*dt:
                self.direction = desiredDirection
            
            if self.direction > 360:
                self.direction -= 360
            elif self.direction < 0:
                self.direction += 360

            distance = self.getDistance(target)

            #update position and rect(i.e. Move him)
            if distance > self.speed*dt:
                #not quite there yet...
                dx = math.cos((self.direction-90)*math.pi/float(180))*self.speed*dt
                dy = math.sin((self.direction-90)*math.pi/float(180))*self.speed*dt
                self.position = (self.position[0]+dx, self.position[1]+dy)
                self.rect.center = self.position

            elif self.direction == desiredDirection:
                #facing the target and close enough to walk there, so position = target (avoids endlessly circling it)
                self.position = (target[0],target[1])
                self.targets.pop()  #go for the next target if there is one



    def walkTo(self,position):
        self.targets = [position]

    def attack(self,unit):  #if we put these here then all types of units will have these even if they don't do anything, and it will make the default behaviour == walk
        self.walkTo(unit.position)
        
    def gather(self,resource):
        self.walkTo(resource.rect.center)
        
    def setAnimation(self, animation):
        if animation in self.animations:
            self.currentanimation = self.animations[animation]
            self.surface = self.currentanimation.reset()    #set the animation back to frame 0

    def interact(self, objects):
        if len(self.targets) > 0:   #only wanna do collision detection/avoidance if we're moving
            for item in objects:
                if item != self and item.__class__ != mapobject.Leaves:    #make sure we're not targetting ourself

                    if self.attackTarget.sprites():
                        if item == self.attackTarget.sprites()[0]:
                            continue    #consider next item

                    try:
                        itemPos = item.position
                    except AttributeError:
                        itemPos = item.rect.center
                    
                    dist = self.getDistance(itemPos)
                    mindist = self.radius + item.radius
                    if dist < mindist:
                        angle = self.getAngleTo(itemPos) - 90 - 180
                        angle *= math.pi/float(180)
                        dx = math.cos(angle)*mindist
                        dy = math.sin(angle)*mindist
                        self.position = (itemPos[0] + dx, itemPos[1] + dy)
                        self.rect.center = self.position
                    

"""                    if circleLineIntersect(itemPos, item.radius, self.position, self.targets[-1]):
                        if isinstance(item, Unit):                    
                            #tell him to get out of the way
                            item.getOutTheWay(self)
                        else:
                            #its not a unit, get out of the way yourself
                            self.getOutTheWay(item)
               
    def getOutTheWay(self, item):
        #calc new target and move there
"""                 
                
class WorkerUnit(Unit):
    animations = {'default': 'worker1'}
    price = 0

    def __init__(self,graphics,position):
        Unit.__init__(self,graphics,position,WorkerUnit.animations)
        self.carrying = False
        self.gatherRange = 20
        self.radius = 25
    def gather(self, resource):
        self.gatherTarget.empty()
        self.gatherTarget.add(resource)
        self.targets = [resource.rect.center]
        
        
    def update(self, dt):
        if self.gatherTarget.sprites(): #there are targets
            resource = (self.gatherTarget.sprites())[0]
            distance = math.sqrt(float((resource.rect.centerx-self.position[0])**2+(resource.rect.centery-self.position[1])**2))
            if distance < self.gatherRange:
                #TODO: make leaf carrying animation
                resource.take()
                self.carrying = True
                self.gatherTarget.empty()
                self.targets = []
        
        Unit.update(self, dt)

class SoldierUnit(Unit):
    animations = {'default': 'soldier1'}
    price = 0

    def __init__(self,graphics,position):
        Unit.__init__(self,graphics,position,SoldierUnit.animations)
        self.attackTime = 1000 #in ms
        self.attackRange = 10
        self.attackPower = 20
        self.attackTimer = stuff.Timer(self.attackTime)
        self.radius = 40
    def attack(self, unit):
        self.attackTarget.empty()
        self.attackTarget.add(unit)
        self.targets = [unit.position]  #set the first element of the list to refer to the target

    def bite(self,unit):
        unit.health -= self.attackPower #TODO give the units a "defense" stat which reduces the strength of the attack by some factor
                                        #ALSO the unit under attack needs to be notified of this
                                        
    def update(self, dt):
        #attack stuff
        if self.attackTarget.sprites(): #there are targets
            enemy = (self.attackTarget.sprites())[0]
            distance = math.sqrt(float((enemy.position[0]-self.position[0])**2+(enemy.position[1]-self.position[1])**2))
            if distance < (self.radius + self.attackRange + enemy.radius):
                #TODO: make attack animation
                #attack enemy
                if self.attackTimer.ready():
                    self.bite(enemy)
                self.targets = []
            else:
                try:
                    self.targets[0] = enemy.position
                except:
                    self.targets = [enemy.position]
        Unit.update(self, dt)
