#-*-coding:utf-8-*-

import curses


__all__ = ['Picker', 'pick']


KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_UP = (curses.KEY_UP, ord('k'))
KEYS_DOWN = (curses.KEY_DOWN, ord('j'))
KEYS_SELECT = (curses.KEY_RIGHT, ord(' '))

class Picker(object):
    """The :class:`Picker <Picker>` object

    :param options: a list of options to choose from
    :param title: (optional) a title above options list
    :param indicator: (optional) custom the selection indicator
    :param default_index: (optional) set this if the default selected option is not the first one
    :param selected_indicator: (option) curses attribute to use when item has been selected
    """

    def __init__(self, options, title=None, indicator='*', default_index=0, selected_indicator=curses.A_BOLD):

        if len(options) == 0:
            raise ValueError('options should not be an empty list')

        self.options = options
        self.title = title
        self.indicator = indicator

        if default_index >= len(options):
            raise ValueError('default_index should be less than the length of options')

        self.selected_indicator = selected_indicator

        self.index = default_index
        self.selected_lines = []
        self.custom_handlers = {}

    def register_custom_handler(self, key, func):
        self.custom_handlers[key] = func

    def move_up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self):
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def select(self):
        if self.index not in self.selected_lines:
            self.selected_lines.append(self.index)
        else:
            self.selected_lines.remove(self.index)

    def get_selected(self):
        """return the current selected options as a list of tuples: (option, index)
        """
        return [(self.options[index], index) for index in self.selected_lines]

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

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        scroll_top = getattr(self, 'scroll_top', 0)
        if current_line <= scroll_top:
            scroll_top = 0
        elif current_line - scroll_top > max_rows:
            scroll_top = current_line - max_rows

        self.scroll_top = scroll_top
        lines_to_draw = lines[scroll_top:scroll_top+max_rows]
        option_lines= self.get_option_lines()

        for line in lines_to_draw:
            current_index = option_lines.index(line) if line in option_lines else -1
            self.screen.addnstr(y, x, line, max_x-2, self.selected_indicator if current_index in self.selected_lines else curses.A_NORMAL)
            y += 1

        self.screen.refresh()

    def run_loop(self):
        while True:
            self.draw()
            c = self.screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_SELECT:
                self.select()
            elif c in KEYS_ENTER:
                return self.get_selected()
            elif c in self.custom_handlers:
                ret = self.custom_handlers[c](self)
                if ret:
                    return ret

    def config_curses(self):
        # use the default colors of the terminal
        curses.use_default_colors()
        # hide the cursor
        curses.curs_set(0)

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        return self.run_loop()

    def start(self):
        return curses.wrapper(self._start)


def pick(options, title=None, indicator='*', default_index=0, selected_indicator=curses.A_BOLD):
    """Construct and start a :class:`Picker <Picker>`.

    Usage::

      >>> from pick import pick
      >>> title = 'Please choose an option: '
      >>> options = ['option1', 'option2', 'option3']
      >>> option, index = pick(options, title)
    """
    picker = Picker(options, title, indicator, default_index, selected_indicator)
    return picker.start()
