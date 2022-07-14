import curses
from pick import Picker
from typing import Tuple


def print_selection(selection):
    if isinstance(selection, list):
        assert len(selection) == 1
        option, index = selection[0]
        print(option, index)
    else:
        print("KEY_LEFT pressed!")


def go_back(picker):
    return (None, -1)

title = 'Please choose your favorite programming language: '
options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']

# with type annotation
picker: Picker[Tuple[None, int], str] = Picker(options, title)
picker.register_custom_handler(curses.KEY_LEFT, go_back)
selection = picker.start()
print_selection(selection)

# with type warning suppression
unannotated_picker = Picker(options, title)  # type: ignore[var-annotated]
unannotated_picker.register_custom_handler(curses.KEY_LEFT, go_back)
selection = picker.start()
print_selection(selection)
