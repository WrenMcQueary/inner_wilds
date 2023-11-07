"""Run this to run the game."""


from source.flowchart_importing import read_game_graph
from source.game_running import run_game_main_loop


if __name__ == "__main__":
    graph = read_game_graph()
    run_game_main_loop(graph)
