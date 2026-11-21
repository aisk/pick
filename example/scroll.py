import os

from pick import pick

title = "Select:"
options = [f"foo.bar{x}.baz" for x in range(1, 71)]
option, index = pick(options, title, backend=os.environ.get("PICK_BACKEND", "curses"))
print(option, index)
