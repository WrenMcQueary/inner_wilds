"""Graph-related classes for game flow.
"""


from source.basic_utils import word_wrap


class Graph:
    """Contains the flow for the full game."""
    def __init__(self, scenes: tuple, choices: tuple):
        self.scenes = scenes
        self.choices = choices


class Scene:
    """Analogous to a node."""
    def __init__(self, id: str, text: str, color: str, is_trick: bool, is_start: bool, is_end: bool):
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
        self.is_world = self.text.startswith("WORLD: ")

    def set_choices_to_ids(self, choices_to_ids: tuple):
        """
        Set the attribute choices_to_ids
        :param choices_to_ids:      a tuple of the ids of all choices leading to this scene
        """
        self.choices_to_ids = choices_to_ids

    def set_choices_from_ids(self, choices_from_ids: tuple):
        """
        Set the attribute choices_from_ids
        :param choices_from_ids:    a tuple of the ids of all choices leading away from this scene
        """
        self.choices_from_ids = choices_from_ids

    def set_choices_to_references(self, choices_to_references: tuple):
        """
        Set the attribute choices_to_references
        :param choices_to_references:   a tuple of all Choice objects leading to this scene
        """
        self.choices_to_references = choices_to_references

    def set_choices_from_references(self, choices_from_references: tuple):
        """
        Set the attribute choices_from_references
        :param choices_from_references: a tuple of all Choice objects leading away from this scene
        """
        self.choices_from_references = choices_from_references

    def set_gives_tricks(self, tricks: tuple):
        """
        Set the tricks that this Scene gives.
        :param tricks:  tuple of strings.  Tricks that this Scene gives the player
        :return:
        """
        self.gives_tricks = tricks

    def make_player_choose(self, found_tricks: set):
        """Get a choice from the player and return it.
        :param found_tricks:        set of tricks that have been discovered by the player, as strings
        """
        available_choices = [choice for choice in self.choices_from_references if choice.is_available(found_tricks) and not choice.leads_to_reference.is_trick]
        num_to_choice = {str(cc+1): choice for cc, choice in enumerate(available_choices)}
        prompt = "\n"
        keys = num_to_choice.keys()
        for key in keys:
            value = num_to_choice[key]
            prompt += word_wrap(f"\t{key}: {value.text}\n")
        while True:
            player_response = input(prompt)
            if player_response in keys:
                break
            print("Choice not recognized.  Choose again.")
        return num_to_choice[player_response]

    def is_child_of_world(self) -> tuple:
        """
        If this Scene is not a trick and not a world, and is the child of a world through a sequence of choice without
        any blue or green choices, return True and the world scene it's a child of.  Else return False and None.
        :return:        tuple with two elements: a boolean, then a Scene or None.
        """
        if self.is_world or self.is_trick:
            return False, None

        # Search for a world that this is the child of, given the restrictions described in this function's docstring
        visited_scenes = []
        fringe = [self]
        while len(fringe) > 0:
            # Pop a scene to explore from the fringe
            to_explore = fringe.pop(0)
            # Explore that scene; get its neighbors given our restrictions
            neighbor_scenes = [choice.leads_from_reference for choice in to_explore.choices_to_references if choice.color not in ["green", "blue"]]
            # For each of these neighbors, check if it's a world.  Then if it's not in visited_scenes, add it to visited_scenes and then add it to the fringe
            for scene in neighbor_scenes:
                if scene.is_world:
                    return True, scene
                if scene not in visited_scenes:
                    visited_scenes.append(scene)
                    fringe.append(scene)
        return False, None


class Choice:
    """Analogous to an edge."""
    def __init__(self, id: str, text: str, leads_to_id: str, leads_from_id: str, color):
        """
        :param id:                  unique identifier
        :param text:                the text of the choice.
        :param leads_to_id:         id of the Scene this Choice points away from
        :param leads_from_id:       id of the Scene this Choice points toward
        :param color:               color name.  No color is "gray".
        """
        # Handle errors
        # text is empty
        if len(text) == 0:
            raise ValueError("text must not be empty.  Try setting text to 'Continue' instead")

        # Run
        self.id = id
        self.text = text
        self.leads_to_id = leads_to_id
        self.leads_from_id = leads_from_id
        self.color = color

    def set_leads_to_reference(self, leads_to_reference: Scene):
        """
        Set the attribute leads_to_reference
        :param leads_to_reference:      the Scene object that this choice leads to
        """
        self.leads_to_reference = leads_to_reference

    def set_leads_from_reference(self, leads_from_reference: Scene):
        """
        Set the attribute leads_from_reference
        :param leads_from_reference:    the Scene object that this choice leads away from
        """
        self.leads_from_reference = leads_from_reference

    def set_requires_tricks(self, tricks: tuple):
        """
        Set the tricks required for this choice to be visible to the player.
        :param tricks:  tuple of of strings.  Required tricks for this choice to be visible to the player
        :return:
        """
        self.requires_tricks = tricks

    def is_available(self, found_tricks: set) -> bool:
        """
        Return False if this choice is barred by an unknown trick, else True.
        :param found_tricks:        set of tricks that have been discovered by the player, as strings
        """
        for trick in self.requires_tricks:
            if trick not in found_tricks:
                return False
        return True
