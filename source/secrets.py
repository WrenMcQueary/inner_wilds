"""Secrets that make new Choices visible once known."""


class Secret:
    def __init__(self, text: tuple, player_knows: bool):
        self.text = text
        self.player_knows = player_knows


# Initialize all secrets
all_secrets = []    # TODO
