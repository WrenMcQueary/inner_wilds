"""Splash screen ASCII art and welcome message."""


splash_title = r"""

*  .    O  @    ~~~   o    *  .    O  @    ~~~   o    *  .    O
                    ___
 || ||\ || ||\ || ||    || \\    ||    || || ||    || \\  (( \
 || ||\\|| ||\\|| ||==  ||_//    \\ /\ // || ||    ||  ))  \\ 
 || || \|| || \|| ||___ || \\     \V/\V/  || ||__| ||_//  \_))
 
*  .    O  @    ~~~   o    *  .    O  @    ~~~   o    *  .    O
 
"""

splash_message = r"""Welcome aboard, captain!  Please check the readme for instructions on how to play.

(Game will start when song is finished)"""


def display_splash_screen() -> None:
    """
    Print the splash screen.
    """

    print(splash_title)
    print(splash_message)
