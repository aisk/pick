from pick import pick

title = 'Please choose your favorite programming language: '
options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
selection = pick(options, title, indicator='=>', default_index=2)
assert len(selection) == 1
option, index = selection[0]
print(option, index)
