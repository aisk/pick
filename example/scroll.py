#-*-coding:utf-8-*-

from __future__ import print_function

from pick import pick

title = 'Select one: '
options = ['foo.bar%s.baz' % x for x in range(1, 71)]
option, index = pick(options, title).one()
print(option, index)
