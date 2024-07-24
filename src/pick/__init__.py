import curses
import textwrap
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Any, Container, Generic, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union

__all__ = ["Picker", "pick", "Option"]


@dataclass
class Option:
    label: str
    value: Any = None
    description: Optional[str] = None
    enabled: bool = True


KEYS_ENTER = (curses.KEY_ENTER, ord("\n"), ord("\r"))
KEYS_UP = (curses.KEY_UP, ord("k"))
KEYS_DOWN = (curses.KEY_DOWN, ord("j"))
KEYS_SELECT = (curses.KEY_RIGHT, ord(" "))

SYMBOL_CIRCLE_FILLED = "(x)"
SYMBOL_CIRCLE_EMPTY = "( )"

OPTION_T = TypeVar("OPTION_T", str, Option)
PICK_RETURN_T = Tuple[OPTION_T, int]

Position = namedtuple('Position', ['y', 'x'])

@dataclass
class Picker(Generic[OPTION_T]):
    options: Sequence[OPTION_T]
    title: Optional[str] = None
    indicator: str = "*"
    default_index: int = 0
    multiselect: bool = False
    min_selection_count: int = 0
    selected_indexes: List[int] = field(init=False, default_factory=list)
    index: int = field(init=False, default=0)
    screen: Optional["curses._CursesWindow"] = None
    position: Position = Position(0, 0)
    clear_screen: bool = True
    quit_keys: Optional[Union[Container[int], Iterable[int]]] = None

    def __post_init__(self) -> None:
        if len(self.options) == 0:
            raise ValueError("options should not be an empty list")

        if self.default_index >= len(self.options):
            raise ValueError("default_index should be less than the length of options")

        if self.multiselect and self.min_selection_count > len(self.options):
            raise ValueError(
                "min_selection_count is bigger than the available options, you will not be able to make any selection"
            )

        if all(isinstance(option, Option) and not option.enabled for option in self.options):
            raise ValueError(
                "all given options are disabled, you must at least have one enabled option."
            )

        self.index = self.default_index
        option = self.options[self.index]
        if isinstance(option, Option) and not option.enabled:
            self.move_down()

    def move_up(self) -> None:
        while True:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.options) - 1
            option = self.options[self.index]
            if not isinstance(option, Option) or option.enabled:
                break

    def move_down(self) -> None:
        while True:
            self.index += 1
            if self.index >= len(self.options):
                self.index = 0
            option = self.options[self.index]
            if not isinstance(option, Option) or option.enabled:
                break

    def mark_index(self) -> None:
        if self.multiselect:
            if self.index in self.selected_indexes:
                self.selected_indexes.remove(self.index)
            else:
                self.selected_indexes.append(self.index)

    def get_selected(self) -> Union[List[PICK_RETURN_T], PICK_RETURN_T]:
        """return the current selected option as a tuple: (option, index)
        or as a list of tuples (in case multiselect==True)
        """
        if self.multiselect:
            return_tuples = []
            for selected in self.selected_indexes:
                return_tuples.append((self.options[selected], selected))
            return return_tuples
        else:
            return self.options[self.index], self.index

    def get_title_lines(self, *, max_width: int = 80) -> List[str]:
        if self.title:
            return textwrap.fill(self.title, max_width - 2, drop_whitespace=False).split("\n") + [""]
        return []

    def get_option_lines(self) -> List[str]:
        lines: List[str] = []
        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * " "

            if self.multiselect:
                symbol = (
                    SYMBOL_CIRCLE_FILLED
                    if index in self.selected_indexes
                    else SYMBOL_CIRCLE_EMPTY
                )
                prefix = f"{prefix} {symbol}"

            option_as_str = option.label if isinstance(option, Option) else option
            lines.append(f"{prefix} {option_as_str}")

        return lines

    def get_lines(self, *, max_width: int = 80) -> Tuple[List[str], int]:
        title_lines = self.get_title_lines(max_width=max_width)
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self, screen: "curses._CursesWindow") -> None:
        """draw the curses ui on the screen, handle scroll if needed"""
        if self.clear_screen:
            screen.clear()

        y, x = self.position  # start point

        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines(max_width=max_x)

        # calculate how many lines we should scroll, relative to the top
        scroll_top = 0
        if current_line > max_rows:
            scroll_top = current_line - max_rows

        lines_to_draw = lines[scroll_top : scroll_top + max_rows]

        description_present = False
        for option in self.options:
            if isinstance(option, Option) and option.description is not None:
                description_present = True
                break

        title_length = len(self.get_title_lines(max_width=max_x))

        for i, line in enumerate(lines_to_draw):
            if description_present and i > title_length:
                screen.addnstr(y, x, line, max_x // 2 - 2)
            else:
                screen.addnstr(y, x, line, max_x - 2)
            y += 1

        option = self.options[self.index]
        if isinstance(option, Option) and option.description is not None:
            description_lines = textwrap.fill(option.description, max_x // 2 - 2).split('\n')

            for i, line in enumerate(description_lines):
                screen.addnstr(i + title_length, max_x // 2, line, max_x - 2)

        screen.refresh()

    def run_loop(
        self, screen: "curses._CursesWindow", position: Position
    ) -> Union[List[PICK_RETURN_T], PICK_RETURN_T]:
        while True:
            self.draw(screen)
            c = screen.getch()
            if self.quit_keys is not None and c in self.quit_keys:
                if self.multiselect:
                    return []
                else:
                    return None, -1
            elif c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                if (
                    self.multiselect
                    and len(self.selected_indexes) < self.min_selection_count
                ):
                    continue
                return self.get_selected()
            elif c in KEYS_SELECT and self.multiselect:
                self.mark_index()

    def config_curses(self) -> None:
        try:
            # use the default colors of the terminal
            curses.use_default_colors()
            # hide the cursor
            curses.curs_set(0)
        except:
            # Curses failed to initialize color support, eg. when TERM=vt100
            curses.initscr()

    def _start(self, screen: "curses._CursesWindow"):
        self.config_curses()
        return self.run_loop(screen, self.position)

    def start(self):
        if self.screen:
            # Given an existing screen
            # don't make any lasting changes
            last_cur = curses.curs_set(0)
            ret = self.run_loop(self.screen, self.position)
            if last_cur:
                curses.curs_set(last_cur)
            return ret
        return curses.wrapper(self._start)


def pick(
    options: Sequence[OPTION_T],
    title: Optional[str] = None,
    indicator: str = "*",
    default_index: int = 0,
    multiselect: bool = False,
    min_selection_count: int = 0,
    screen: Optional["curses._CursesWindow"] = None,
    position: Position = Position(0, 0),
    clear_screen: bool = True,
    quit_keys: Optional[Union[Container[int], Iterable[int]]] = None,
):
    picker: Picker = Picker(
        options,
        title,
        indicator,
        default_index,
        multiselect,
        min_selection_count,
        screen,
        position,
        clear_screen,
        quit_keys,
    )
    return picker.start()
