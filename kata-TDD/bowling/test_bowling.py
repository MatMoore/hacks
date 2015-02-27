import pytest
from bowling import Game


@pytest.fixture
def game():
    return Game()


def test_gutter_game(game):
    for i in xrange(20):
        game.roll(0)
    assert game.score() == 0


def test_all_ones(game):
    for i in xrange(20):
        game.roll(1)
    assert game.score() == 20
