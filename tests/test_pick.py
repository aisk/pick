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

    def test_multi_select(self):
        title = 'Please choose an option: '
        options = ['option1', 'option2', 'option3']
        picker = Picker(options, title, multi_select=True, min_selection_count=1)
        assert picker.get_selected() == []
        picker.mark_index()
        assert picker.get_selected() == [('option1', 0)]
        picker.move_down()
        picker.mark_index()
        assert picker.get_selected() == [('option1', 0), ('option2', 1)]

    def test_options_map(self):
        title = 'Please choose an option: '
        options = [{'label': 'option1'}, {'label': 'option2'}, {'label': 'option3'}]

        def get_label(option): return option.get('label')

        picker = Picker(options, title, indicator='*', options_map=get_label)
        lines, current_line = picker.get_lines()
        assert lines == [title, '', '* option1', '  option2', '  option3']
        assert picker.get_selected() == ({ 'label': 'option1' }, 0)

    def test_multi_select_colors(self):
        title = 'Please choose an option: '
        options = ['option1', 'option2', 'option3']

        # valid colors
        picker_loaded = False
        try:
            picker = Picker(options, title, multi_select=True, min_selection_count=1, multi_select_foreground_color='COLOR_BLUE', multi_select_background_color='COLOR_MAGENTA')
            picker_loaded = True
        except:
            picker_loaded = False
        assert picker_loaded == True

        # invalid foreground color
        picker_loaded = False
        try:
            picker = Picker(options, title, multi_select=True, min_selection_count=1, multi_select_foreground_color='pantone 505')
            picker_loaded = True
        except ValueError:
            picker_loaded = False
        assert picker_loaded == False

        # invalid background color
        picker_loaded = False
        try:
            picker = Picker(options, title, multi_select=True, min_selection_count=1, multi_select_foreground_color='pantone 15-0343')
            picker_loaded = True
        except ValueError:
            picker_loaded = False
        assert picker_loaded == False



if __name__ == '__main__':
    unittest.main()
