import os
import data

class animation:
    def __init__(self, graphics, animationname, extension='.png'):
        self.images = []
        
        files = os.listdir(data.filepath('images/'animationname+'/');
        files.sort()
        for frameNum in files:
            self.images.append(graphics.loadImage(animationname+'/'+frameNum)

        self.framenum = 0
        self.accumulator = 0.0
        self.max = 1/float(FRAMERATE)

    def update(self, dt):
        self.accumulator += dt
        if self.accumulator > self.max:
            self.framenum += 1
            if self.framenum > len(self.images):
                self.framenum = 0
            self.accumulator -= self.max
        return self.images[self.framenum]
