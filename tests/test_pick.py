#-*-coding:utf-8-*-

import unittest
from pick import Picker


class TestPick(unittest.TestCase):

    def test_move_up_down(self):
        title = 'Please choose an option: '
        options = ['option1', 'option2', 'option3']
        picker = Picker(options, title)
        picker.move_up()
        assert picker.get_selected() == ('option3', 2)
        picker.move_down()
        picker.move_down()
        assert picker.get_selected() == ('option2', 1)

    def test_default_index(self):
        title = 'Please choose an option: '
        options = ['option1', 'option2', 'option3']
        picker = Picker(options, title, default_index=1)
        assert picker.get_selected() == ('option2', 1)

    def test_get_lines(self):
        title = 'Please choose an option: '
        options = ['option1', 'option2', 'option3']
        picker = Picker(options, title, indicator='*')
        lines, current_line = picker.get_lines()
        assert lines == [title, '', '* option1', '  option2', '  option3']
        assert current_line == 3

    def test_no_title(self):
        options = ['option1', 'option2', 'option3']
        picker = Picker(options)
        lines, current_line = picker.get_lines()
        assert current_line == 1

    def test_choose_one(self):
        options = ['option1', 'option2', 'option3']
        picker = Picker(options)
    	option1_index = options.index('option1')
    	picker.chosen_options = [option1_index]
        assert picker.get_chosen() == ('option1', option1_index)

    def test_choose_many(self):
        options = ['option1', 'option2', 'option3']
        picker = Picker(options)
    	picker.multiselect_allow = True
    	option2_index = options.index('option2')
    	option3_index = options.index('option3')
    	picker.chosen_options = [option2_index, option3_index]
        assert picker.get_chosen() == [('option2', option2_index), ('option3', option3_index)]

if __name__ == '__main__':
    unittest.main()
