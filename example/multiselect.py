#-*-coding:utf-8-*-

from __future__ import print_function

from pick import Picker

title = 'Please choose some foo bars: '
options = ['foo.bar%s.baz' % x for x in range(1, 50)]

picker = Picker(options, title)
selected = picker.start()
print([str(option[0]) for option in selected])
