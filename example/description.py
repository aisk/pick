from pick import pick

title = "Please choose your favorite programming language: "
options = ["Java", "JavaScript", "Python", "PHP", "C++", "Erlang", "Haskell"]
descriptions = ["Java is a high-level, class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible. It is a general-purpose programming language intended to let programmers write once, run anywhere (WORA), meaning that compiled Java code can run on all platforms that support Java without the need to recompile.",
                "JavaScript, often abbreviated as JS, is a programming language and core technology of the Web, alongside HTML and CSS. Almost every website uses JavaScript on the client side for webpage behavior.",
                "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.",
                "PHP is a general-purpose scripting language geared towards web development.",
                "C++ is a high-level, general-purpose programming language created by Danish computer scientist Bjarne Stroustrup, first released in 1985 as an extension of the C programming language.",
                "",
                ""
]
option, index = pick(options, title, descriptions, indicator="=>", default_index=2)
print(f"You choosed {option} at index {index}")