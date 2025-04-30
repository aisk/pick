from pick import pick

title = "Select:"
options = [f"foo.bar{x}.baz" * 100 for x in range(1, 71)]
option, index = pick(options, title)
print(option, index)
