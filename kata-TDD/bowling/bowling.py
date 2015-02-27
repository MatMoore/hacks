class Game(object):
    def __init__(self):
        self.current_frame = None
        self.frames = []

    def roll(self, number):
        if self.current_frame is not None:
            self.frames.append((self.current_frame, number))
            self.current_frame = None
        elif number == 10:
            self.frames.append((number,))
        else:
            self.current_frame = number

    def score(self):
        total = 0
        num_frames = len(self.frames)
        for frame_number in xrange(0, num_frames):
            frame = self.frames[frame_number]
            total += sum(frame)

            try:
                next_frame = self.frames[frame_number + 1]
            except IndexError:
                pass
            else:
                if self.is_spare(frame):
                    total += self.spare_bonus(next_frame)
                elif self.is_strike(frame):
                    total += self.strike_bonus(next_frame)

        return total

    def is_spare(self, frame):
        return len(frame) == 2 and sum(frame) == 10

    def is_strike(self, frame):
        return len(frame) == 1 and sum(frame) == 10

    def spare_bonus(self, next_frame):
        return next_frame[0]

    def strike_bonus(self, next_frame):
        return sum(next_frame)
