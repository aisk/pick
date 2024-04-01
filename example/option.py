from pick import pick, Option

title = "Please choose your favorite programming language: "
options = [
    Option("Java", ".java"),
    Option("Python", ".py"),
    Option("JavaScript", ".js"),
]
option, index = pick(options, title)
print(f"You chose {option} at index {index}")
