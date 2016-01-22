#-*-coding:utf-8-*-

import curses


__all__ = ['Picker', 'pick']


KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_UP = (curses.KEY_UP, ord('k'))
KEYS_DOWN = (curses.KEY_DOWN, ord('j'))
KEYS_SEARCH = (ord('/'),)


class Picker(object):
    """The :class:`Picker <Picker>` object

    :param options: a list of options to choose from
    :param title: (optional) a title above options list
    :param indicator: (optional) custom the selection indicator
    :param default_index: (optional) set this if the default selected option is not the first one
    """

    def __init__(self, options, title=None, indicator='*', default_index=0, search=''):

        if len(options) == 0:
            raise ValueError('options should not be an empty list')

        self._options = options
        self.title = title
        self.indicator = indicator
        self.search = search
        self._search_mode = False

        if default_index >= len(options):
            raise ValueError('default_index should be less than the length of options')

        self.index = default_index

    @property
    def options(self):
        return [opt for opt in self._options if self.search.lower() in opt.lower()]

    def move_up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self):
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def get_selected(self):
        """return the current selected option as a tuple: (option, index)
        """
        return self.options[self.index], self.index

    def get_title_lines(self):
        if self.title:
            return self.title.split('\n') + ['']
        return []

    def get_option_lines(self):
        lines = []

        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * ' '
            line = '{0} {1}'.format(prefix, option)
            lines.append(line)

        return lines

    def get_lines(self):
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self):
        """draw the curses ui on the screen, handle scroll if needed"""
        self.screen.clear()

        x, y = 1, 1  # start point
        max_y, max_x = self.screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw
        if self.search:
            max_rows = max_rows - 1

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        scroll_top = getattr(self, 'scroll_top', 0)
        if current_line <= scroll_top:
            scroll_top = 0
        elif current_line - scroll_top > max_rows:
            scroll_top = current_line - max_rows
        self.scroll_top = scroll_top

        lines_to_draw = lines[scroll_top:scroll_top+max_rows]

        for line in lines_to_draw:
            self.screen.addstr(y, x, line)
            y += 1

        self.screen.addstr(max_y - 1, 1, self.search)

        self.screen.refresh()

    def run_loop(self):
        while True:
            self.draw()
            c = self.screen.getch()

            if self._search_mode:
                if c in KEYS_ENTER:
                    self._search_mode = False
                    continue
                self.search += chr(c)

            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                return self.get_selected()
            elif c in KEYS_SEARCH:
                self.search = ''
                self.index = 0
                self._search_mode = not self._search_mode

    def config_curses(self):
        # use the default colors of the terminal
        curses.use_default_colors()
        # hide the cursor
        curses.curs_set(0)

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        return self.run_loop()

    def start(self):
        return curses.wrapper(self._start)


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
