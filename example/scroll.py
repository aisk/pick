import os

from pick import pick

title = "Select:"
options = ["foo.bar%s.baz" % x for x in range(1, 71)]
option, index = pick(options, title, backend=os.environ.get("PICK_BACKEND", "curses"))
print(option, index)
