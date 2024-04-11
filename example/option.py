from pick import pick, Option

title = "Please choose your favorite programming language: "
options = [
    Option("Python", ".py", "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation."),
    Option("Java", description="Java is a high-level, class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible. It is a general-purpose programming language intended to let programmers write once, run anywhere (WORA), meaning that compiled Java code can run on all platforms that support Java without the need to recompile."),
    Option("JavaScript", ".js"),
    Option("C++")
]
option, index = pick(options, title, indicator="=>")
print(f"You chose {option} at index {index}")
