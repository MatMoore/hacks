#TODO

#all units inherit from a basic unit class, which inherits from mapobject

#have some basic stats
#and a state (what they are currently doing)

#need an interact method which takes a list of visible stuff, and the unit changes its state as appropriate

import pygame

class Unit(MapObject):
    """Base class for units (anything which can move)"""
    def __init__(self,surface,position):
        MapObject.__init__(self)
        self.action = None
        self.health = 100
        self.speed = 10
        self.target = None #walk target
        self.attackTarget = None
        self.attackRate = 1

    def isDead(self):
        return self.health <= 0

    def move(self,dt):
        '''If they are walking towards something keep moving'''
        if self.target:
            pass

        #if target is in range, stop and attack

    def attack(self,unit):
        pass

    def walkTo(self,position):
        pass
