import os
import data
from constants import *

class Animation:
    def __init__(self, graphics, animationname):
        self.images = []
        
        files = os.listdir(data.filepath('images/'+animationname+'/'))
        files.sort()
        for filename in files:
            self.images.append(graphics.loadImage(animationname+'/'+filename))

        self.framenum = 0
        self.accumulator = 0.0
        self.max = 1/float(FRAMERATE)

    def update(self, dt):
        self.accumulator += dt
        if self.accumulator > self.max:
            self.framenum += 1
            if self.framenum >= len(self.images):
                self.framenum = 0
            self.accumulator -= self.max
        return self.images[self.framenum]
        
    def reset(self):
        """resets frame and accumulator to 0 and returns the first frame"""
        self.accumulator = 0.0
        self.framenum = 0
        return self.images[self.framenum]
