import pytest
from bowling import Game


class GameHelper(Game):
    """
    Add some helper functions to our game for testing
    """
    def roll_many(self, n, pins):
        for i in xrange(n):
            self.roll(pins)

    def roll_spare(self, first=5):
        self.roll(first)
        self.roll(10 - first)


@pytest.fixture
def game():
    return GameHelper()


def test_gutter_game(game):
    game.roll_many(20, pins=0)
    assert game.score() == 0


def test_all_ones(game):
    game.roll_many(20, pins=1)
    assert game.score() == 20


def test_one_spare(game):
    game.roll_spare()
    game.roll(3)
    game.roll_many(17, pins=0)
    assert game.score() == 16


#def test_strike(game):
#    game.roll(10)
#    game.roll(3)
#    game.roll(4)
