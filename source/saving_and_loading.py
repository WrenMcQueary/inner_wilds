"""For saving and loading the game."""


import os


SHIP_LOG_PATH = "ship_log.txt"
SHIP_LOG_HEADER = "--------LOG BEGINS BELOW--------\n"
LOG_ENTRY_SIGNIFIER = "LOG ENTRY: "


def is_save_file_missing() -> bool:
    """
    Check if the save file is missing entirely.
    :return:    True if the save file does not exist, else False
    """
    return not os.path.isfile(SHIP_LOG_PATH)


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
        file.write(SHIP_LOG_HEADER)
        for trick in tricks_found:
            file.write(f"{LOG_ENTRY_SIGNIFIER}{trick}\n")


def load() -> tuple:
    """
    Load the game from the ship log.
    :return:    tuple with (scene id, set of tricks found)
    """
    # If no ship log, create a blank one
    if is_save_file_missing():
        wipe_save()

    # Load
    with open(SHIP_LOG_PATH, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        content = content.split("\n")
        scene_id = content[0].replace("current scene id: ", "")
        tricks = set()
        for line in content[3:]:
            if line.startswith(LOG_ENTRY_SIGNIFIER):
                tricks.add(line[len(LOG_ENTRY_SIGNIFIER):])
        return (scene_id, tricks)
    except:
        raise RuntimeError(f"Unfortunately the current state of your save file ({SHIP_LOG_PATH}) is invalid.  You'll have to start a new game.")
