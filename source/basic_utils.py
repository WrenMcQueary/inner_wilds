"""Handling really basic stuff, below even the level of scenes and choices."""


def word_wrap(s: str, line_length=80) -> str:
    """
    Intersperse s with newlines so that it doesn't run off the player's screen so easily when printed.
    Split on spaces whenever able
    :param s:               string to be processed
    :param line_length:     maximum character count between newlines
    :return:
    """
    chunks = []

    unchunked = s
    del s

    while len(unchunked) > 0:
        if len(unchunked) <= line_length:
            chunks.append(unchunked)
            unchunked = ""
        elif "\n" in unchunked[:line_length]:
            newline_index = unchunked.index("\n")
            chunks.append(unchunked[:newline_index])
            unchunked = unchunked[newline_index+1:]
        else:
            # Get the line_length'th character of unchunked
            index_to_chunk = line_length
            char_to_chunk = unchunked[index_to_chunk]
            # Get the nearest space at or before this character
            while char_to_chunk != " ":
                index_to_chunk -= 1
                if index_to_chunk <= 0:     # If no spaces found, give up and treat all that remains as a chunk
                    chunks.append(unchunked)
                    unchunked = ""
                char_to_chunk = unchunked[index_to_chunk]
            # Chunk on that entire contiguous collection of spaces
            leftmost_space_index = index_to_chunk   # index of the leftmost space
            rightmost_space_index = index_to_chunk + 1  # index of the character *after* the rightmost space
            while leftmost_space_index > 0 and unchunked[leftmost_space_index-1] == " ":
                leftmost_space_index -= 1
            while rightmost_space_index <= len(unchunked)-1 and unchunked[rightmost_space_index] == " ":
                rightmost_space_index += 1
            chunks.append(unchunked[:leftmost_space_index])
            unchunked = unchunked[rightmost_space_index:]

    # Recompose chunks into a string and return
    out = "\n".join(chunks)
    return out


def make_player_choose(prompt: str, options: dict) -> str:
    """
    Show a player a prompt and a numbered collection of options, then force them to pick a valid number.
    :param prompt:      the prompt to show.
    :param options:     a dict of options to show, with their numbers as keys.  For example, {"1": "Eat the bread", "2": "Smell the bread", "3": "Drop the bread"}
    :return:            the number the player chose
    """
    print(word_wrap(prompt) + "\n")
    prompt = ""
    for key, value in options.items():
        prompt += word_wrap(f"    {key}: {value}\n")
    prompt += "\n    "
    while True:
        player_response = input(prompt)
        if player_response in options:
            return player_response
        print(word_wrap("Choice not recognized.  Press a number for one of the following options, then press Enter."))
