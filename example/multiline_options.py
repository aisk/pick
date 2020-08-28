#-*-coding:utf-8-*-

from __future__ import print_function

import curses
from pick import Picker

def go_back(picker):
    return (None, -1)

title = 'Please choose your favorite NBA trio: '
options = [
    'Bill Russell\nBob Cousy\nJohn Havlicek',
    'Magic Johnson\nKareem Abdul Jabbar\nJames Worthy',
    'Larry Bird\nKevin McHale\nRobert Parrish',
    'Michael Jordan\nScottie Pippen\nDennis Rodman',
    'Walt Frazier\nWillis Reed\nDave DeBusschere',
    'Tim Duncan\nManu Ginobili\nTony Parker'
]

picker = Picker(options, title, indicator='---->', multiselect=True)
picker.register_custom_handler(curses.KEY_LEFT, go_back)
option, index = picker.start()
print(option, index)