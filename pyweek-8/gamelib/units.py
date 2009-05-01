import math
import random
import pygame
import animation
import mapobject
import stuff
import pathfinder
from constants import *

def vecadd(a, b):
    try:
        return (a[0] + b[0], a[1] + b[1])
    except:
        return (a[0] + b, a[1] + b)

def vecdel(a, b):
    return (a[0] - b[0], a[1] - b[1])
    
def vecmul(a, b):
    try:
        return (a[0] * b[0], a[1] * b[1])
    except:
        return (a[0] * b, a[1] * b)
    
def vecdot(a, b):
    return a[0] * b[0] + a[1] * b[1]
    
def vecnorm(a):
    length = math.sqrt(a[0]**2 + a[1]**2)
    return (a[0]/length, a[1]/length)
    
    
#TODO: make an idle behaviour method - e.g. workers should seek out leaves
def intersectCircleSegment(c,r,p1,p2):
    dirr = vecdel(p2, p1)
    diff = vecdel(c, p1)
    try:
        t = float(vecdot(diff, dirr)) / float(vecdot(dirr, dirr))
    except ZeroDivisionError:
        return False
    
    if (t < 0.0):
        t = 0.0
    if (t > 1.0):
        t = 1.0
        
    closest = vecadd(p1, vecmul(dirr, t))
    d = vecdel(c,closest)
    distsqr = vecdot(d, d)
    return distsqr <= r*r



class Unit(mapobject.MapObject):
    """Base class for units (anything which can move)"""
    price = 0

    def __init__(self, graphics, position, animations):
        self.position = position
        self.health = 100
        self.maxHealth = 100
        self.speed = 25
        self.targets = [] #walk target
        self.seekTarget = pygame.sprite.Group()   #i've kept these here so that the collision avoidance can check
        self.attackTarget = pygame.sprite.Group()   #whether this unit is just trying to move or whether it's doing
                                                    #something useful - maybe there's a better way

        self.animations = dict()
        for action,anim in animations.iteritems():
            self.animations[action] = animation.Animation(graphics, anim)
        
        self.currentanimation = self.animations['default']  #set us to the default animation
        mapobject.MapObject.__init__(self, self.currentanimation.reset(), position) #init the base class with the first frame of the animation
        self.direction = 100
        
        self.pathFinder = pathfinder.PathFinder(self.radius)
    
    def randomWalk(self, target, averagedistance = 200):
        distance = self.getDistance(target)
        numberofnodes = math.floor(distance/200) -1 # -1 because the target node is set outside the loop
        vector = vecdel(target, self.position)
        vector = vecnorm(vector)
        vector = vecmul(vector, 0-averagedistance)  #multiplied by 0-average distance because we're going back from the end
        currentpos = target
        targets = []
        
        #must add the target so here
        randompos = (currentpos[0] + random.randint(0,averagedistance)-100, currentpos[1] + random.randint(0,averagedistance)-100)
        targets.append(randompos)        
        
        for i in range(numberofnodes):
            currentpos = vecadd(currentpos, vector)
            randompos = (currentpos[0] + random.randint(0,averagedistance)-100, currentpos[1] + random.randint(0,averagedistance)-100)
            targets.append(randompos)


        return targets
        
    
    
    def getDistance(self, target):
        """get the distance from current location to target"""
        return math.sqrt(float((target[0]-self.position[0])**2+(target[1]-self.position[1])**2))


    def changeAnimation(self,anim):
        if anim in self.animations:
            self.currentanimation = self.animations[anim]

    def fixAngle(self, angle, angle2 = None):
        """returns angle with a distance of no more than 180 from self.direction or angle2 - to correct for the discontinuity of 360 == 0"""
        if angle2 == None:
            angle2 = self.direction
        while abs(angle - angle2) > 180:
            if angle2 < angle:
                angle -= 360
            elif  angle2 > angle:
                angle += 360
        return angle

    def getAngleTo(self, target):
        result = math.atan2(target[1]-self.position[1], target[0]-self.position[0])*180/math.pi
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
            desiredDirection = self.fixAngle(desiredDirection)
            
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
            if distance > 15:   #15 is roughly the turning radius
                #not quite there yet...
                dx = math.cos((self.direction)*math.pi/float(180))*self.speed*dt
                dy = math.sin((self.direction)*math.pi/float(180))*self.speed*dt
                self.position = (self.position[0]+dx, self.position[1]+dy)
                self.rect.center = self.position

            elif self.direction == desiredDirection:
                #facing the target and close enough to walk there, so position = target (avoids endlessly circling it)
                self.targets.pop()  #go for the next target if there is one



    def walkTo(self,position):
#        self.targets = [position]
#        self.targets = self.pathFinder.calcPath(self.position, position)
         self.targets = self.randomWalk(position)
         
    def attack(self,unit):  #if we put these here then all types of units will have these even if they don't do anything, and it will make the default behaviour == walk
        self.walkTo(unit.position)
        
    def gather(self,resource,colony):
        self.walkTo(resource.rect.center)
        
    def setAnimation(self, animation):
        if animation in self.animations:
            self.currentanimation = self.animations[animation]
            self.surface = self.currentanimation.reset()    #set the animation back to frame 0

    def interact(self, objects):
        self.pathFinder.clearUp()   #delete all the moveable units from the pathfinder - leave only the solid things
        for item in objects:

            if self.attackTarget.sprites():
                if item == self.attackTarget.sprites()[0]:
                    continue    #consider next item

            if item != self and item.__class__ != mapobject.Leaves:    #make sure we're not targetting ourself
                
                try:
                    itemPos = item.position
                except AttributeError:
                    itemPos = item.rect.center
                        
                self.pathFinder.addObstacle(itemPos, item.radius)   #currently adding everything as non-permanent, no memory                


                if len(self.targets) > 0:   #only wanna do collision detection/avoidance if we're moving
                   
                   
                    dist = self.getDistance(itemPos)
                    minDist = self.radius + item.radius
                    angleTo = self.getAngleTo(itemPos)
                    
                    #collisions
                    if dist < minDist:
                        angle = (angleTo-180)*math.pi/float(180)
                        dx = math.cos(angle)*minDist
                        dy = math.sin(angle)*minDist
                        self.position = (itemPos[0] + dx, itemPos[1] + dy)
                        self.rect.center = self.position
                        itemTargetDistance = float((self.targets[-1][0]-itemPos[0])**2+(self.targets[-1][1]-itemPos[1])**2)
                        if itemTargetDistance < minDist**2:
                            self.targets.pop()
                            break

                    if dist < (minDist + AVOIDDISTANCE):
#                        randomTarget = (self.position[0] + random.randint(-100,100), self.position[1] + random.randint(-100,100))

                        #find a random target in a sector facing away from the thing
                        fixAng = self.fixAngle(angleTo)
                        if fixAng < self.direction:
                            angle = angleTo + 45
                        else:
                            angle = angleTo - 45

                        while True:
                            randomAngle = random.uniform(-RANDOMTARGETMAXANGLE,RANDOMTARGETMAXANGLE)
                            if randomAngle > RANDOMTARGETMINANGLE:
                                randomAngle = (randomAngle + angle) % 2*math.pi
                                break

                        while True:
                            randomDist = math.sqrt(random.random())*RANDOMTARGETMAX #this ensures that the random targets are uniformly spread out over the sector
                            if randomDist > RANDOMTARGETMIN:
                                break

                        randomTarget = (randomDist*math.cos(randomAngle*180/math.pi),randomDist*math.sin(randomAngle*180/math.pi))

                        if len(self.targets) > 1:
                            if intersectCircleSegment(itemPos, item.radius, self.position, self.targets[-1]):
                                self.targets[-1] = randomTarget
                        else:
                            self.targets.append(randomTarget)
                        
                        #checks whether our final target is within the unit and if it is then stay where we are.
                        itemTargetDistance = float((self.targets[-1][0]-itemPos[0])**2+(self.targets[-1][1]-itemPos[1])**2)
                        if itemTargetDistance < item.radius**2:
                            self.targets.pop()
                            break
                
class WorkerUnit(Unit):
    animations = {'default': 'worker1', 'carrying':'worker2'}
    price = 0

    def __init__(self,graphics,position):
        Unit.__init__(self,graphics,position,WorkerUnit.animations)
        self.carrying = False
        #self.gatherRange = 20
        self.radius = 25

    def gather(self, resource, colony):
        self.seekTarget.empty()
        self.seekTarget.add(colony)
        self.seekTarget.add(resource)
        self.targets = [resource.rect.center]
        
        
    def update(self, dt):
        if len(self.seekTarget)>1: 
            colony = None
            leaves = None
            for i in self.seekTarget: #yeah this sucks
                if i.__class__ is mapobject.Colony:
                    colony = i
                elif i.__class__ is mapobject.Leaves:
                    leaves = i
                if colony and leaves:
                    break

            if colony and leaves:
                if self.carrying and pygame.sprite.collide_circle(self,colony): #we are back at the colony
                    colony.addLeaves(1)
                    self.carrying = False
                    print "return"
                    self.setAnimation('default')
                    self.targets = [leaves.rect.center]

                elif not self.carrying and pygame.sprite.collide_circle(self,leaves):
                    leaves.take()
                    self.carrying = True
                    print "carrying"
                    self.setAnimation('carrying')
                    self.targets = [colony.rect.center]
        
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
