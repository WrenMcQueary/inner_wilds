"""For running the game proper"""


from source.graph import Graph, Scene, Choice


def run_game_main_loop(graph: Graph) -> None:
    """
    Run the game.  Repeatedly show the user a scene and request a choice, until the game ends.  Keep track of tricks
    that the player uncovers.
    :param graph:   Graph object representing the full game
    """
    # Initialize list of found tricks
    # TODO

    # Find the START node.  Throw an error if there isn't exactly one.
    # TODO

    # Find the node that the START node points to.  Throw an error if there isn't exactly one.  Make it the active scene
    # TODO

    # Play the intro song
    # TODO

    # Main loop
    while True:
        # Show the user the active scene
        # TODO

        # Determine the choices that should be visible to the player from this scene, given the tricks they have
        # TODO

        # Get the user to make a choice
        # TODO

        # Change the active scene
        # TODO

        # Unlock any tricks related to this new active scene
        # TODO

        # If the active scene is an end scene, end the game
        # TODO
