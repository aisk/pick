from pick import pick, Option

title = "Please choose an option: "
options = [
    Option("Option 1", description="All options are `enabled` by default.", enabled=False),
    Option("Option 2", description="You can change that by changing the `enabled` attribute of the `Option` object to `False`."),
    Option("Option 3", description="This option is disabled!"),
    Option("Option 4", description="Moving up and down, skips over the disabled options.", enabled=False)
]
option, index = pick(options, title, indicator="=>")
print(f"You chose {option} at index {index}")
