from pick import pick

title = "Please choose your favorite programming language: "
options = ["Java", "JavaScript", "Python", "PHP", "C++", "Erlang", "Haskell"]
option, index = pick(options, title, indicator="=>", default_index=2)
print(f"You choosed {option} at index {index}")
