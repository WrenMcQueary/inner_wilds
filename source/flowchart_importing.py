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
        # Color
        if "color" in this_dict:
            this_color = color_number_to_name(this_dict["color"])
        else:
            this_color = color_number_to_name(this_dict[None])
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
            this_color = color_number_to_name(this_dict[None])
        # Requires tricks
        this_requires_tricks = TODO     # TODO
        # Gives tricks
        this_gives_tricks = TODO       # TODO
        # Build and append to output
        out.append(Choice(this_id, this_text, this_leads_to, this_leads_from, this_color, this_requires_tricks, this_gives_tricks))
        pass

    return out


def read_game_graph() -> Graph:
    """Read the canvas file"""
    with open(FLOWCHART_PATH) as file:
        content = json.load(file)
    scenes = content["nodes"]
    # TODO: Turn scenes from a list of dicts to a list of Scene objects, using build_scene_objects()
    choices = content["edges"]
    # TODO: Turn choices from a list of dicts to a list of Choice objects, using build_choice_objects()
    game_graph = Graph(scenes, choices)
    return game_graph
