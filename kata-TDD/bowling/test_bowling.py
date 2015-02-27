from bowling import Game


def test_gutter_game():
    game = Game()
    for i in xrange(20):
        game.roll(0)
    assert game.score() == 0
