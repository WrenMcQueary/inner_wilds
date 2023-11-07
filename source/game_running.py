"""For running the game proper"""


from source.graph import Graph, Scene, Choice
from source.basic_utils import word_wrap
from source.flowchart_syntax import trick_signifier


def run_game_main_loop(graph: Graph) -> None:
    """
    Run the game.  Repeatedly show the user a scene and request a choice, until the game ends.  Keep track of tricks
    that the player uncovers.
    :param graph:   Graph object representing the full game
    """
    # Initialize list of found tricks
    found_tricks = set()

    # Find the START node.  Throw an error if there isn't exactly one.
    start_nodes = []
    for scene in graph.scenes:
        if scene.is_start:
            start_nodes.append(scene)
    if len(start_nodes) != 1:
        raise RuntimeError("number of START nodes must be exactly 1")
    start_node = start_nodes[0]
    del start_nodes

    # Find the node that the START node points to.  Throw an error if there isn't exactly one.  Make it the active scene
    if len(start_node.choices_from_references) != 1:
        raise RuntimeError("the START node must point to exactly 1 scene")
    active_scene = start_node.choices_from_references[0].leads_to_reference

    # Play the intro song
    # TODO

    # Main loop
    while True:
        print("\n" + "-"*80 + "\n")

        # Show the user the active scene
        print(word_wrap(active_scene.text))

        # Get the user to make a choice
        player_choice = active_scene.make_player_choose(found_tricks)

        # Change the active scene
        active_scene = player_choice.leads_to_reference

        # Unlock any tricks related to this new active scene
        for choice in active_scene.choices_from_references:
            if choice.leads_to_reference.is_trick:
                trick = choice.leads_to_reference.text[len(trick_signifier):]
                found_tricks.add(trick)

        # If the active scene is an end scene, end the loop
        if active_scene.is_end:
            break
