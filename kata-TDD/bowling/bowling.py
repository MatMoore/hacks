class Game(object):
    def __init__(self):
        self._score = 0

    def roll(self, number):
        self._score += number

    def score(self):
        return self._score
