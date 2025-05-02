from pick import pick
from blessed.terminal import Terminal

title = "Select (begin typing to filter options):"
options = [f"foo.bar{x}.baz" * 100 for x in range(1, 71)]
option, index = pick(options, title, pagination_color=Terminal().green)
print(option, index)
