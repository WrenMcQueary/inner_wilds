"""For saving and loading the game."""


SHIP_LOG_PATH = "ship_log.txt"


def is_save_data_empty() -> bool:
    """
    Check if the save data is empty.
    :return:    True if the save file is empty, else False
    """
    with open(SHIP_LOG_PATH, "r", encoding="utf-8") as file:
        content = file.read()
    return len(content) == 0


def wipe_save() -> None:
    """Empty the ship log."""
    with open(SHIP_LOG_PATH, "w", encoding="utf-8") as file:
        file.write("")


def save(scene_id: str, tricks_found: set) -> None:
    """
    Save the game to the ship log path.
    :param scene_id:
    :param tricks_found:
    :return:
    """
    with open(SHIP_LOG_PATH, "w", encoding="utf-8") as file:
        file.write(f"current scene id: {scene_id}\n")
        file.write("\n")
        file.write(f"--------LOG BEGINS BELOW--------\n")
        for trick in tricks_found:
            file.write(f"LOG ENTRY: {trick}\n")


def load() -> tuple:
    """
    Load the game from the ship log.
    :return:    tuple with (scene id, set of tricks found)
    """
    with open(SHIP_LOG_PATH, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        content = content.split("\n")
        scene_id = content[0].replace("current scene id: ", "")
        tricks = set()
        for line in content[3:]:
            tricks.add(line)
        return (scene_id, tricks)
    except:
        raise RuntimeError("The ship log (which doubles as your save file) was corrupted.  You'll have to start a new game.")
