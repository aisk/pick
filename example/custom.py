import curses
from pick import Picker

def go_back(picker):
    return (None, -1)

title = 'Please choose your favorite programming language: '
options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']

picker = Picker(options, title)
picker.register_custom_handler(curses.KEY_LEFT, go_back)
option, index = picker.start()
print(option, index)
