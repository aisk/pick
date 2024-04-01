from pick import pick

title = "Please choose your favorite programming language: "
options = {
    "Java": "Java is a high-level, class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible. It is a general-purpose programming language intended to let programmers write once, run anywhere (WORA), meaning that compiled Java code can run on all platforms that support Java without the need to recompile.",
    "JavaScript": "JavaScript, often abbreviated as JS, is a programming language and core technology of the Web, alongside HTML and CSS. Almost every website uses JavaScript on the client side for webpage behavior.",
    "Python": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.",
    "PHP": "PHP is a general-purpose scripting language geared towards web development.",
    "C++": "C++ is a high-level, general-purpose programming language created by Danish computer scientist Bjarne Stroustrup, first released in 1985 as an extension of the C programming language.",
    "Erlang": "",
    "Haskell": ""
}
option, index = pick(options, title, indicator="=>", default_index=5)
print(f"You chose {option} at index {index}")
