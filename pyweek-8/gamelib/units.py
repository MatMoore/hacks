#TODO

#all units inherit from a basic unit class, which inherits from mapobject

#have some basic stats
#and a state (what they are currently doing)

#need an interact method which takes a list of visible stuff, and the unit changes its state as appropriate
import math
import pygame
import animation
import mapobject
from constants import *
class Unit(mapobject.MapObject):
    """Base class for units (anything which can move)"""
    price = 0

    def __init__(self, graphics, position, animations):
        self.position = position
        self.action = None
        self.health = 100
        self.speed = 25
        self.target = None #walk target
        self.attackTarget = None
        self.attackRate = 1
        self.animations = dict()
        
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
        pass

    def walkTo(self,position):
        self.target = position
        
    def setAnimation(self, animation):
        if animation in self.animations:
            self.currentanimation = self.animations[animation]
            self.surface = self.currentanimation.reset()    #set the animation back to frame 0
