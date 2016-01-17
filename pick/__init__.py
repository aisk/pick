#-*-coding:utf-8-*-

import curses


__all__ = ['Picker', 'pick']


KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_UP = (curses.KEY_UP, ord('k'))
KEYS_DOWN = (curses.KEY_DOWN, ord('j'))


class Picker(object):
    """The :class:`Picker <Picker>` object

    :param options: a list of options to choose from
    :param title: (optional) a title above options list
    :param indicator: (optional) custom the selection indicator
    :param default_index: (optional) set this if the default selected option is not the first one
    """

    def __init__(self, options, title=None, indicator='*', default_index=0):

        if len(options) == 0:
            raise ValueError('options should not be an empty list')

        self.options = options
        self.title = title
        self.indicator = indicator

        if default_index >= len(options):
            raise ValueError('default_index should be less than the length of options')

        self.index = default_index

    def move_up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1
        self.draw()

    def move_down(self):
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0
        self.draw()

    def get_selected(self):
        """return the current selected option as a tuple: (option, index)
        """
        return self.options[self.index], self.index

    def draw(self):
        """draw the curses ui on the screen"""
        self.screen.clear()

        x, y = 1, 1
        if self.title:
            self.screen.addstr(y, x, self.title)
            y += 2

        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * ' '
            line = '{0} {1}'.format(prefix, option)
            self.screen.addstr(y, x, line)
            y += 1

        self.screen.refresh()

    def start(self):
        return curses.wrapper(self.run_loop)

    def config_curses(self):
        # use the default colors of the terminal
        curses.use_default_colors()
        # hide the cursor
        curses.curs_set(0)

    def run_loop(self, screen):
        self.config_curses()
        self.screen = screen
        self.draw()

        while True:
            c = self.screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                return self.get_selected()


def pick(options, title=None, indicator='*', default_index=0):
    """Construct and start a :class:`Picker <Picker>`.

    Usage::

      >>> from pick import pick
      >>> title = 'Please choose an option: '
      >>> options = ['option1', 'option2', 'option3']
      >>> option, index = pick(options, title)
    """
    picker = Picker(options, title, indicator, default_index)
    return picker.start()
