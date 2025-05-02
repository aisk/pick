from pick import pick
from typing import List
from blessed.keyboard import get_curses_keycodes # type: ignore

keystrokes = get_curses_keycodes()

# https://blessed.readthedocs.io/en/latest/keyboard.html
# KEY_EXIT is the escape key
QUIT_KEYS: List[int] = [ord("q"), keystrokes["KEY_EXIT"], keystrokes["KEY_F1"]]

title = "Please choose your favorite programming language: "
options = ["Java", "JavaScript", "Python", "PHP", "C++", "Erlang", "Haskell"]
option, index = pick(
    options, title, indicator="=>", default_index=2, quit_keys=QUIT_KEYS
)
print(f"You chose {option} at index {index}")
