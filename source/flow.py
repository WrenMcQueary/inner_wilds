"""Graph-related classes for game flow.
"""


class Graph:
    """Contains the flow for the full game."""
    def __init__(self, scenes: tuple, choices: tuple):
        self.scenes = scenes
        self.choices = choices


class Scene:
    """Analogous to a node."""
    def __init__(self, text: str, choices_from: tuple):
        self.text = text
        self.choices_from = choices_from

    def make_player_choose(self):
        """Get a choice from the player and return it."""
        available_choices = [choice for choice in self.choices_from if choice.is_available()]
        num_to_choice = {str(cc+1): choice for cc, choice in enumerate(available_choices)}
        prompt = ""
        keys = num_to_choice.keys()
        for key in keys:
            value = num_to_choice[key]
            prompt += f"{key}: {value}\n"
        while True:
            player_response = input(prompt)
            if player_response in keys:
                break
            print("Choice not recognized.  Choose again.")
        return num_to_choice[player_response]


class Choice:
    """Analogous to an edge."""
    def __init__(self, text: str, leads_to: Scene, requires_secrets=tuple(), gives_secrets=tuple()):
        self.text = text
        self.leads_to = leads_to
        self.requires_secrets = requires_secrets
        self.gives_secrets = gives_secrets

    def is_available(self) -> bool:
        """Return False if this choice is barred by an unknown secret, else True.
        """
        for secret in self.requires_secrets:
            if not secret.player_knows:
                return False
        return True
