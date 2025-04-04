# Inner Wilds

A little text-based game inspired by [Outer Wilds](https://store.steampowered.com/app/753640/Outer_Wilds/), for the love of my life.

## Installation

### Windows
To play the game, run the file `main.exe`.  No installation required!

### Other operating systems
You'll need to run the game's Python source.  Here's how:
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/#next-steps), a Python package manager.
2. Open a terminal at this repository's root.
3. Run `uv sync` to create a Python virtual environment and install all Python dependencies.
4. If you're on Linux or macOS, run `source .venv/bin/activate` to activate the environment.  On Windows systems, you'll need to run `.venv\Scripts\activate` instead.
5. Run `python3 main.py` to launch the game.

## How to play

There's a little bit of music at the start of the game, so turn your volume on.  ^^

`ship_log.txt` will contain a log of important things you've learned, and items you've picked up.  It also doubles as your save file.  The game autosaves every time you perform an action.

To quit, press Ctrl + C or close the game window or terminal.

## How to make your own games
I made the underlying graph for this game using [Obsidian Canvas](https://obsidian.md/canvas), and built a parser that turns Obsidian Canvas graphs into playable text-adventure games!  You can edit the graph to make your own text-based adventure game.  Download Obsidian [here](https://obsidian.md/download) to view and edit the graph.

Here's a quick primer on how to control your game's behavior using the graph.

### Scenes and choices
The graph consists of scenes (aka nodes, boxes) and choices (aka edges, arrows, connectors).  Almost all scenes contain text that is displayed to the player, and almost all choices determine the options available to a player, which move them to different scenes.

If you label a choice, that label will be visible to the player when they are deciding which choice to pick.  You can leave up to one outgoing choice per scene blank and it will automatically receive the label "Continue".

### Color determines behavior, except gray and purple
The color of scenes and choices has significance in determining the behavior of your graph.  Your scenes and choices should be the gray default color (leftmost on the Obsidian Canvas palette), unless you want to invoke any of the behaviors described below.

However, purple scenes and choices elicit the same behavior as gray ones.  Feel free to use gray and purple however you see fit for organizational purposes.  I like to use purple for major locations that aren't quite hubs.

### Start and end nodes
Every story has a beginning.  To determine which scene is first presented to the player, create a red scene with the label "START", and draw a normal-colored choice from it to your desired scene.

Every story has at least one ending, too.  To determine which choice(s) end the game, create one or more red scenes with the label "END", and direct your desired into them.

Your graph can have only one start node, but it can have multiple end nodes.

### Hubs
Many stories are structured around hub areas that can be quickly returned to.  You can implement this by creating a blue scene for your hub.  Any scene downstream of your hub will automatically have an additional outgoing choice when the game runs, which will lead back to your hub.  You do not need to create these additional choices in your graph; the game will do that for you.

Of course, during certain important moments, you may wish to remove the player's ability to return to a hub.  You can use blue choices to achieve this, cutting off upstream travel from the current scene back to the hub scene.  

### Gating progress
You can prevent certain choices from appearing until the player has obtained one or more prerequisites, such as items or key pieces of knowledge.  These prerequisites are called *tricks*. The game engine automatically keeps track of them in the player's save file, and displays them in a human-readable way, allowing the player to review their progress so far.

When a player performs an action that should gain them a trick, you should draw a connector from that scene to a new green node.  This green node must begin with the text "TRICK: ", followed by a summary of what the player has gained.  When the player reaches the node before the trick node, this summary will be written to the save file, rather than displayed as a scene in that moment.

The trick node should have an outgoing green connector pointing to any scenes it unlocks new choices for.  The unlockable choices must be yellow.  A yellow choice will only become available to the player once all green edges pointing into its source node have had their tricks gained by the player.

### Scene state
Sometimes the player may perform an action that changes a scene.  Perhaps the scene text should change, or the choices offered at that scene should change, or both.  In the graph, this is implemented as making the choices that would normally lead to that scene instead reroute to a new one.

You can direct orange connectors from tricks to normal scenes.  If the player would reach a scene where all tricks connected to it by orange connectors have been fulfilled, they will instead skip the scene and be sent to a new scene, determined by an outgoing orange connector from the original scene.

A state can redirect to only one other state, but you can implement a chain of state redirects with unlimited length.

### Changing other game elements
These changes won't affect your `main.exe` file until you recompile it.
- **Splash screen:** Edit the `splash_title` variable in `source/splash.py`
- **Splash screen song:** Replace `source/audio/Inner Wilds.mp3` with a different mp3 file.
- **Name of the save file, save file header, or prefix of save file trick entries:** Edit the `SHIP_LOG_PATH`, `SHIP_LOG_HEADER`, and/or `LOG_ENTRY_SIGNIFIER` variables in `source/saving_and_loading.py`.
- **Choice text for returning to a hub**: Edit the `HUB_RETURN_CHOICE_STRING` variable in `source/flowchart_importing.py`.

## Recompiling the exe
Recompiling the exe can only be performed on Windows.  Recompiling is necessary to apply certain changes to `main.exe`, but if you're just running Python instead, it's never necessary.

On a Windows machine, you can recompile with the terminal command `pyinstaller main.py`.  If you used `uv sync` to set up a virtual environment for this repository and activated it with `.venv\Scripts\activate`, you will already be able to run PyInstaller.

Finally, delete `_internal/` and `main.exe`, and replace them with their counterparts found inside `dist/main/`.
