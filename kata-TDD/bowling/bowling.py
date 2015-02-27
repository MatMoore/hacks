class Game(object):
    def __init__(self, max_frames=10):
        self.current_frame = None
        self.frames = []
        self.max_frames = max_frames

    @property
    def reached_last_frame(self):
        return len(self.frames) == self.max_frames

    @property
    def started_frame(self):
        return self.current_frame is not None

    def start_frame(self, number):
        self.current_frame = number

    def end_frame(self, number):
        self.frames.append((self.current_frame, number))
        self.current_frame = None

    def add_frame(self, frame):
        self.frames.append(frame)

    def extend_frame(self, number):
        # On the last frame, we may make extra rolls
        # if there are strikes/spares
        self.frames[-1] += (number,)

    def roll(self, number):
        if self.started_frame:
            self.end_frame(number)
        elif self.reached_last_frame:
            self.extend_frame(number)
        elif number == 10:
            self.add_frame((number,))
        else:
            self.start_frame(number)

    def score(self):
        total = 0
        num_frames = len(self.frames)
        for frame_number in xrange(0, num_frames):
            frame = self.frames[frame_number]
            remaining = self.frames[frame_number + 1:]
            total += sum(frame)

            if self.is_spare(frame):
                total += self.spare_bonus(remaining)
            elif self.is_strike(frame):
                total += self.strike_bonus(remaining)

        return total

    def is_spare(self, frame):
        return len(frame) == 2 and sum(frame) == 10

    def is_strike(self, frame):
        return len(frame) == 1 and sum(frame) == 10

    def spare_bonus(self, remaining):
        return remaining[0][0] if remaining else 0

    def rolls(self, frames):
        for frame in frames:
            for roll in frame:
                yield roll

    def strike_bonus(self, remaining):
        next_rolls = self.rolls(remaining)
        try:
            first = next_rolls.next()
            second = next_rolls.next()
        except StopIteration:
            # Bonus is as yet unknown
            return 0
        return first + second
