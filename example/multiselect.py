from pick import pick

title = "Choose your favorite programming language(use space to select)"
options = ["Java", "JavaScript", "Python", "PHP", "C++", "Erlang", "Haskell"]
selected = pick(options, title, multiselect=True, min_selection_count=1)
print(selected)
