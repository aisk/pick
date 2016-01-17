#-*-coding:utf-8-*-

import unittest
from pick import pick, Picker


class TestPick(unittest.TestCase):

    def test_pick(self):
        title = 'Please choose an option: '
        options = ['option1', 'option2', 'option3']
        picker = Picker(options, title)
        picker.move_up()
        assert picker.get_selected() == ('option3', 2)
        picker.move_down()
        picker.move_down()
        assert picker.get_selected() == ('option2', 1)


if __name__ == '__main__':
    unittest.main()
