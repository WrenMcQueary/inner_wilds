"""For reading the game flowchart, which is stored as an Obsidian .canvas file so that it can be easily edited and
redesigned.
"""


import json
from os import path
from source.graph import Graph, Scene, Choice


FLOWCHART_PATH = path.join("source", "game_flowchart.canvas")


def color_number_to_name(color_number) -> str:
    """
    Given a color number or None, return the name of the associated color.
    :param color_number:    str or None
    :return:                string name of the associated color, in lowercase
    """
    conversion_dict = {
        None: "gray",
        "1": "red",
        "2": "orange",
        "3": "yellow",
        "4": "green",
        "5": "blue",
        "6": "purple",
    }
    try:
        return conversion_dict[color_number]
    except KeyError:
        raise ValueError(f"color_number not recognized: {color_number}")


def build_scene_objects(scene_dicts: list) -> list:
    """
    Convert a list of scene dicts read from the flowchart canvas file to Scene objects.
    :param scene_dicts:     list of scene dicts read from the flowchart canvas file.
    :param choice_dicts:    list of choice dicts read from the flowchart canvas file.
    :return:                list of Scene objects, one for each scene dict
    """
    out = []

    for this_dict in scene_dicts:
        # Id
        this_id = this_dict["id"]
        # Text
        this_text = this_dict["text"]
        if len(this_text) == 0:
            this_text = "Continue"
        # Color
        if "color" in this_dict:
            this_color = color_number_to_name(this_dict["color"])
        else:
            this_color = color_number_to_name(None)
        # Is trick
        this_is_trick = this_text.startswith("TRICK: ") and this_color == "green"
        # Is start
        this_is_start = this_text == "START" and this_color == "red"
        # Is end
        this_is_end = this_text == "END" and this_color == "red"
        # Build and append to output
        out.append(Scene(this_id, this_text, this_color, this_is_trick, this_is_start, this_is_end))

    return out


def build_choice_objects(choice_dicts: list) -> list:
    """
    Convert a list of choice dicts read from the flowchart canvas file to Choice objects.
    :param scene_dicts:     list of scene dicts read from the flowchart canvas file.
    :param choice_dicts:    list of choice dicts read from the flowchart canvas file.
    :return:                list of Choice objects, one for each choice dict
    """
    out = []

    for this_dict in choice_dicts:
        # Id
        this_id = this_dict["id"]
        # Text
        if "label" in this_dict:
            this_text = this_dict["label"]
        else:
            this_text = "Continue"
        # Leads to
        this_leads_to = this_dict["toNode"]
        # Leads from
        this_leads_from = this_dict["fromNode"]
        # Color
        if "color" in this_dict:
            this_color = color_number_to_name(this_dict["color"])
        else:
            this_color = color_number_to_name(None)
        # Build and append to output
        out.append(Choice(this_id, this_text, this_leads_to, this_leads_from, this_color))
        pass

    return out


def read_game_graph() -> Graph:
    """Read the canvas file"""
    # Get scenes and choices from the canvas file
    with open(FLOWCHART_PATH) as file:
        content = json.load(file)
    scenes = content["nodes"]
    choices = content["edges"]

    # Convert them to Scene and Choice objects
    scenes = build_scene_objects(scenes)
    choices = build_choice_objects(choices)

    # Set choices_to_ids, choices_to_references, choices_from_ids, and choices_from_references for all Scenes
    # choices_to_ids and choices_to_references
    for scene in scenes:
        choices_to_ids = []
        choices_to_references = []
        for choice in choices:
            if choice.leads_to_id == scene.id:
                choices_to_ids.append(choice.id)
                choices_to_references.append(choice)
        scene.set_choices_to_ids(tuple(choices_to_ids))
        scene.set_choices_to_references(tuple(choices_to_references))
    # choices_from_ids and choices_from_references
    for scene in scenes:
        choices_from_ids = []
        choices_from_references = []
        for choice in choices:
            if choice.leads_from_id == scene.id:
                choices_from_ids.append(choice.id)
                choices_from_references.append(choice)
        scene.set_choices_from_ids(tuple(choices_from_ids))
        scene.set_choices_from_references(tuple(choices_from_references))

    # Set leads_to_reference and leads_from_reference for all Choices
    for choice in choices:
        # leads_to_reference
        for scene in scenes:
            if scene.id == choice.leads_to_id:
                choice.set_leads_to_reference(scene)
                break
        # leads_from_reference
        for scene in scenes:
            if scene.id == choice.leads_from_id:
                choice.set_leads_from_reference(scene)
                break

    # For all Scenes, set gives_tricks
    trick_signifier = "TRICK: "
    for scene in scenes:
        gives_tricks = []
        for choice in scene.choices_from_references:
            text = choice.leads_to_reference.text
            if text.startswith(trick_signifier):
                gives_tricks.append(text[len(trick_signifier):])
        scene.set_gives_tricks(tuple(gives_tricks))

    # For all Choices, set requires_tricks
    for choice in choices:
        requires_tricks = []
        relevant_scene = choice.leads_from_reference
        if choice.color == "yellow":
            for inbound_choice in relevant_scene.choices_to_references:
                if inbound_choice.color == "green" and inbound_choice.leads_from_reference.text.startswith(trick_signifier):
                    requires_tricks.append(inbound_choice.leads_from_reference.text[len(trick_signifier):])
            choice.set_requires_tricks(tuple(requires_tricks))
        else:
            choice.set_requires_tricks(tuple())

    # Build the game Graph
    game_graph = Graph(scenes, choices)
    return game_graph
