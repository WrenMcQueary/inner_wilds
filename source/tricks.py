"""Tricks that make new Choices visible once acquired.
Tricks represent knowledge or items that unlock new possibilities in the game.
"""


class Trick:
    def __init__(self, text: tuple, player_knows: bool):
        self.text = text
        self.player_knows = player_knows


# Initialize all tricks
all_tricks = []    # TODO
