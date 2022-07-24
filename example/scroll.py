from pick import pick

title = "Select:"
options = ["foo.bar%s.baz" % x for x in range(1, 71)]
selection = pick(options, title)
assert len(selection) == 1
option, index = selection[0]
print(option, index)
