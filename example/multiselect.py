#-*-coding:utf-8-*-

from __future__ import print_function

from pick import Picker

title = 'Please select your favourite flavours of ice cream: '
options = ['Chocolate', 'Cookies and Cream', 'Vanilla', 'Cookie Dough', 'Mint Chocolate Chip', 'Strawberry', 'Rocky Road', 'Butter Pecan', 'Coffee']

picker = Picker(options, title)
selected = picker.start()

if selected:
	print('Your favourite flavours: {0} - good choice!'.format(', '.join([str(option[0]) for option in selected])))
else:
	print('No ice cream flavours selected :-(')
