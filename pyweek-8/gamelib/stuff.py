import pygame
class Timer:
    '''Could probably use a pygame timer or something else for this but oh well this is simpler maybe'''
    def __init__(self,period):
        self.period = period
        self.last = pygame.time.get_ticks() - period

    def ready(self):
        '''Return true if its time for the event to happen'''
        now = pygame.time.get_ticks()
        if now-self.last > self.period:
            self.last = now
            return True
        else:
            return False
