"""For reading the game flowchart, which is stored as an Obsidian .canvas file so that it can be easily edited and
redesigned.
"""


import json
from os import path
from source.flow import Graph, Scene, Choice


FLOWCHART_PATH = path.join("source", "game_flowchart.canvas")


def read_game_graph() -> Graph:
    """Read the canvas file"""
    with open(FLOWCHART_PATH) as file:
        content = json.load(file)
    scenes = content["nodes"]
    choices = content["edges"]
    game_graph = Graph(scenes, choices)
    return game_graph
