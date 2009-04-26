#TODO

#all units inherit from a basic unit class, which inherits from mapobject

#have some basic stats
#and a state (what they are currently doing)

#need an interact method which takes a list of visible stuff, and the unit changes its state as appropriate

import pygame
import animation
import mapobject

class Unit(mapobject.MapObject):
    """Base class for units (anything which can move)"""
    price = 0

    def __init__(self, graphics, position, animations):
        self.position = position
        self.action = None
        self.health = 100
        self.speed = 10
        self.target = None #walk target
        self.attackTarget = None
        self.attackRate = 1
        self.animations = dict()
        
        for anim in animations:
            self.animations[anim] = animation.Animation(graphics, anim)
        
        self.currentanimation = self.animations[animations[0]]  #set us to the first animation
        mapobject.MapObject.__init__(self, self.currentanimation.reset(), position) #init the base class with the first frame of the animation

    def isDead(self):
        return self.health <= 0

    def update(self,dt):
        #continue animation    
        self.surface = self.currentanimation.update(dt)

        #keep moving if walking towards something
        if self.target:
            #work out direction
            #update position
            #update rect
            pass

        #if target is in range, stop and attack

    def attack(self,unit):
        pass

    def walkTo(self,position):
        pass
        
    def setAnimation(self, animation):
        if animation in self.animations:
            self.currentanimation = self.animations[animation]
            self.surface = self.currentanimation.reset()    #set the animation back to frame 0
