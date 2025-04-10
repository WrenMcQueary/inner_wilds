"""For running the game proper"""


from source.graph import Graph
from source.basic_utils import make_player_choose
from source.flowchart_syntax import trick_signifier
from source.saving_and_loading import is_save_file_missing, is_save_data_empty, wipe_save, save, load
from source.splash import display_splash_screen

from playsound3 import playsound


SCENE_DIVIDER = "\n" + "-" * 80 + "\n"


def get_initial_game_state() -> tuple:
    """
    Either continue an existing game or start a new game, at the player's choice.
    :return:    tuple with (scene id, set of tricks found) to pick up the game.  If we should start a new game, return ("", set())
    """
    # If the ship log is empty, start a new game
    if is_save_file_missing() or is_save_data_empty():
        return "", set()

    # Else, ask the player
    print(SCENE_DIVIDER)
    player_response = make_player_choose("Existing save data detected.  Welcome back, captain.  Would you like to continue your game or start over?", {"1": "Continue", "2": "Delete save data and start new game"})
    if player_response == "2":
        print(SCENE_DIVIDER)
        player_response = make_player_choose("Last chance -- delete your save data for good?", {"1": "Keep my save data and continue my existing game", "2": "Delete my save data and start over"})
        if player_response == "2":
            wipe_save()
            return "", set()
        return load()
    return load()


def run_game_main_loop(graph: Graph) -> None:
    """
    Run the game.  Repeatedly show the user a scene and request a choice, until the game ends.  Keep track of tricks
    that the player uncovers.
    :param graph:   Graph object representing the full game
    """
    # Start a new game or pick up from a save
    starting_scene_id, found_tricks = get_initial_game_state()
    if len(starting_scene_id) == 0:     # If new game...
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
        # Title screen and play the intro song
        display_splash_screen()
        playsound("source/audio/Inner Wilds.mp3")
    else:   # If continuing a saved game...
        # Find the scene to make active
        active_scene = None
        for scene in graph.scenes:
            if scene.id == starting_scene_id:
                active_scene = scene
                break
        if active_scene is None:
            raise RuntimeError(f"Loading saved game failed; couldn't find a scene matching the scene id in save file: {starting_scene_id}")

    # Main loop
    while True:
        print(SCENE_DIVIDER)

        # Show the user the active scene and get the user to make a choice
        player_choice = active_scene.present_scene_and_make_player_choose(found_tricks)

        # Change the active scene
        active_scene = player_choice.leads_to_reference

        # Redirect to a state variant of this scene if needed
        should_redirect = True
        if active_scene.has_state_variant():
            for choice in active_scene.choices_to_references:
                if choice.color == "orange" and choice.leads_from_reference.is_trick:
                    trick = choice.leads_from_reference
                    if trick.text[len(trick_signifier):] not in found_tricks:
                        should_redirect = False
        else:
            should_redirect = False
        if should_redirect:
            outgoing_oranges = [choice for choice in active_scene.choices_from_references if choice.color == "orange"]
            if len(outgoing_oranges) != 1:
                raise RuntimeError(f"Cannot redirect to state variant of scene {active_scene.id} because does not have exactly 1 outgoing orange edge.")
            active_scene = outgoing_oranges[0].leads_to_reference

        
        # Unlock any tricks related to this new active scene
        for choice in active_scene.choices_from_references:
            if choice.leads_to_reference.is_trick:
                trick = choice.leads_to_reference.text[len(trick_signifier):]
                found_tricks.add(trick)

        # If the active scene is an end scene, end the loop
        if active_scene.is_end:
            break

        # Save
        save(active_scene.id, found_tricks)
