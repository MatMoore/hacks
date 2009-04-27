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
class Unit(mapobject.MapObject):
    """Base class for units (anything which can move)"""
    price = 0

    def __init__(self, graphics, position, animations):
        self.position = position
        self.health = 100
        self.maxHealth = 100
        self.speed = 25
        self.target = None #walk target
        self.attackTarget = pygame.sprite.Group()
        self.attackTime = 1000 #in ms
        self.attackRange = 20
        self.attackPower = 20
        self.animations = dict()
        self.attackTimer = stuff.Timer(self.attackTime)
        
        for anim in animations:
            self.animations[anim] = animation.Animation(graphics, anim)
        
        self.currentanimation = self.animations[animations[0]]  #set us to the first animation
        mapobject.MapObject.__init__(self, self.currentanimation.reset(), position) #init the base class with the first frame of the animation
        self.direction = 100
        
        
    def isDead(self):
        return self.health <= 0

    def update(self,dt):
        #continue animation    
        self.surface = self.currentanimation.update(dt)

        #attack stuff
        if self.attackTarget.sprites(): #there are targets
            enemy = (self.attackTarget.sprites())[0]
            distance = math.sqrt(float((enemy.position[0]-self.position[0])**2+(enemy.position[1]-self.position[1])**2))
            if distance < self.attackRange:
                #TODO: make attack animation
                #attack enemy
                if self.attackTimer.ready():
                    self.bite(enemy)
                self.target = None
            else:
                self.target=enemy.position

        #keep moving if walking towards something
        if self.target:
        
            #calculate desired heading
            desiredDirection = math.atan2(self.target[1]-self.position[1], self.target[0]-self.position[0])
            desiredDirection = desiredDirection * 180/math.pi + 90
            if desiredDirection < 0:
                desiredDirection += 360
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

            distance = math.sqrt(float((self.target[0]-self.position[0])**2+(self.target[1]-self.position[1])**2))

            #update position and rect(i.e. Move him)
            if distance > self.speed*dt:
                #not quite there yet...
                dx = math.cos((self.direction-90)*math.pi/float(180))*self.speed*dt
                dy = math.sin((self.direction-90)*math.pi/float(180))*self.speed*dt
                self.position = (self.position[0]+dx, self.position[1]+dy)
                self.rect.left = self.position[0]
                self.rect.top = self.position[1]

            elif self.direction == desiredDirection:
                #facing the target and close enough to walk there, so position = target (avoids endlessly circling it)
                self.position = (self.target[0],self.target[1])
                self.target = None

        #if target is in range, stop and attack

    def attack(self,unit):
        self.attackTarget.add(unit)

    def walkTo(self,position):
        self.target = position

    def bite(self,unit):
        unit.health -= self.attackPower #TODO give the units a "defense" stat which reduces the strength of the attack by some factor
                                        #ALSO the unit under attack needs to be notified of this
        
    def setAnimation(self, animation):
        if animation in self.animations:
            self.currentanimation = self.animations[animation]
            self.surface = self.currentanimation.reset()    #set the animation back to frame 0
