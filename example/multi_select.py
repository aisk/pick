#-*-coding:utf-8-*-

from __future__ import print_function

from pick import pick

title = 'Please choose your favorite programming language: '
options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
selected_options = pick(options, title, indicator='=>', multi_select=True, multi_select_foreground_color='COLOR_BLUE')
print(selected_options)
