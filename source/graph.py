"""Graph-related classes for game flow.
"""


class Graph:
    """Contains the flow for the full game."""
    def __init__(self, scenes: tuple, choices: tuple):
        self.scenes = scenes
        self.choices = choices


class Scene:
    """Analogous to a node."""
    def __init__(self, id: str, text: str, color: tuple, is_trick: bool, is_start: bool, is_end: bool):
        """
        :param id:              unique identifier
        :param text:            the text of the node in the canvas (usually text to be displayed to the player)
        :param color:           color name.  No color is "gray".
        :param is_trick:        Whether this is a TRICK that the player can uncover
        :param is_start:        Whether this is the START node
        :param is_end:          Whether this is an END node
        """
        # Handle errors
        # text is empty
        if len(text) == 0:
            raise ValueError("text must not be empty")

        # Run
        self.id = id
        self.text = text
        self.color = color
        self.is_trick = is_trick
        self.is_start = is_start
        self.is_end = is_end

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
    def __init__(self, id: str, text: str, leads_to: str, leads_from: str, color, requires_tricks=tuple(), gives_tricks=tuple()):
        """
        :param id:                  unique identifier
        :param text:                the text of the choice.
        :param leads_to:            id of the Scene this Choice points away from
        :param leads_from:          id of the Scene this Choice points toward
        :param color:               color name.  No color is "gray".
        :param requires_tricks:     tuple of required tricks for this choice to be visible to the player
        :param gives_tricks:        tuple of tricks that this choice gives the player
        """
        # Handle errors
        # text is empty
        if len(text) == 0:
            raise ValueError("text must not be empty.  Try setting text to 'Continue' instead")

        # Run
        self.id = id
        self.text = text
        self.leads_to = leads_to
        self.leads_from = leads_from
        self.color = color
        self.requires_tricks = requires_tricks
        self.gives_tricks = gives_tricks

    def is_available(self) -> bool:
        """Return False if this choice is barred by an unknown trick, else True.
        """
        for trick in self.requires_tricks:
            if not trick.player_knows:
                return False
        return True
