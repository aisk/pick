#!/usr/bin/env python

from typing import List
from blessed import Terminal
from blessed.keyboard import get_curses_keycodes # type: ignore
import pick

pick.SELECT_KEYS = []

options: List[pick.OPTION_T] = [
    pick.Option(
        "Option 1",
        "value_field",
        "Description field is printed, too (this option is disabled)",
        enabled=False,
    ),
    "option 2",
    "option 3",
    pick.Option("Option 4", "value", "This option is green", color=Terminal().green),
    "option 5",
    pick.Option(
        "Option 6",
        "value",
        "This is a colored but disabled option",
        enabled=False,
        color=Terminal().pink,
    ),
    "option 7",
]

prompt = (
    "(Up/down/tab to move; space to select/de-select; Enter to continue; "
    + "To filter options, simply begin typing)"
)

# Note that the disabled choices are dark grey by default, but can be
# a custom color via the disabled_color= option:
choice = pick.pick(
    options,
    prompt,
    indicator="=>",
    multiselect=True,
    min_selection_count=2,
    quit_keys=[ord("q")],
    select_keys=[get_curses_keycodes()["KEY_RIGHT"]],
    disabled_color=Terminal().gray35,
)

print(f"You chose: {choice}")
