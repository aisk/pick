#-*-coding:utf-8-*-

from __future__ import print_function

from pick import pick

title = 'Please choose your favorite programming language: '
options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
option, index = pick(options, title, indicator='=>', default_index=2).one()
print(option, index)
