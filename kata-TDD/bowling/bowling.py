class Game(object):
    def __init__(self):
        self.rolls = []

    def roll(self, number):
        self.rolls.append(number)

    @property
    def complete_frames(self):
        return zip(self.rolls[::2], self.rolls[1::2])

    def score(self):
        total = 0
        frames = self.complete_frames
        for frame_number in xrange(0, len(frames)):
            frame = frames[frame_number]
            total += sum(frame)

            try:
                next_frame = frames[frame_number + 1]
            except IndexError:
                pass
            else:
                if self.is_spare(frame):
                    total += next_frame[0]

        return total

    def is_spare(self, frame):
        return sum(frame) == 10
