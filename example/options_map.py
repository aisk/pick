#-*-coding:utf-8-*-

from __future__ import print_function

from pick import pick

title = 'Please choose your favorite fruit: '
options = [
    { 'name': 'Apples', 'grow_on': 'trees' },
    { 'name': 'Oranges', 'grow_on': 'trees' },
    { 'name': 'Strawberries', 'grow_on': 'vines' },
    { 'name': 'Grapes', 'grow_on': 'vines' },
]

def get_description_for_display(option):
    # format the option data for display
    return '{0} (grow on {1})'.format(option.get('name'), option.get('grow_on'))

option, index = pick(options, title, indicator='=>', options_map=get_description_for_display)
print(option, index)
