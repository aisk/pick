from pick import pick

KEY_CTRL_C = 3
KEY_ESCAPE = 27
QUIT_KEYS = (KEY_CTRL_C, KEY_ESCAPE, ord("q"))

title = "Please choose your favorite programming language: "
options = ["Java", "JavaScript", "Python", "PHP", "C++", "Erlang", "Haskell"]
option, index = pick(
    options, title, indicator="=>", default_index=2, quit_keys=QUIT_KEYS
)
print(f"You chose {option} at index {index}")
