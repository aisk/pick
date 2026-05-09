import curses
import textwrap
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Any, Container, Generic, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union

from .backend import Backend
from .blessed_backend import BlessedBackend
from .curses_backend import CursesBackend

__all__ = [
    "Picker",
    "pick",
    "Option",
    "Position",
    "Backend",
    "CursesBackend",
    "BlessedBackend",
    "SYMBOL_CIRCLE_FILLED",
    "SYMBOL_CIRCLE_EMPTY",
]


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
KEYS_BACKSPACE = (curses.KEY_BACKSPACE, 127, 8)

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
    backend: Union[str, Backend] = "curses"
    enable_search: bool = False
    _search_string: str = field(init=False, default="")

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
        self._ensure_valid_selection()

    def _ensure_valid_selection(self) -> None:
        filtered = self.get_filtered_options()
        if not filtered:
            return
        if self.index >= len(filtered):
            self.index = 0
        _, option = filtered[self.index]
        if isinstance(option, Option) and not option.enabled:
            self.move_down()

    def get_filtered_options(self) -> List[Tuple[int, OPTION_T]]:
        if not self.enable_search or not self._search_string:
            return list(enumerate(self.options))

        query = self._search_string.lower()
        filtered = []
        for i, opt in enumerate(self.options):
            label = opt.label if isinstance(opt, Option) else str(opt)
            if query in label.lower():
                filtered.append((i, opt))
        return filtered

    def move_up(self) -> None:
        filtered = self.get_filtered_options()
        if not filtered:
            self.index = 0
            return
        while True:
            self.index -= 1
            if self.index < 0:
                self.index = len(filtered) - 1
            _, option = filtered[self.index]
            if not isinstance(option, Option) or option.enabled:
                break

    def move_down(self) -> None:
        filtered = self.get_filtered_options()
        if not filtered:
            self.index = 0
            return
        while True:
            self.index += 1
            if self.index >= len(filtered):
                self.index = 0
            _, option = filtered[self.index]
            if not isinstance(option, Option) or option.enabled:
                break

    def mark_index(self) -> None:
        filtered = self.get_filtered_options()
        if not filtered:
            self.index = 0
            return
        if self.index >= len(filtered):
            self.index = 0
        orig_index, _ = filtered[self.index]
        if self.multiselect:
            if orig_index in self.selected_indexes:
                self.selected_indexes.remove(orig_index)
            else:
                self.selected_indexes.append(orig_index)

    def get_selected(self) -> Union[List[PICK_RETURN_T], PICK_RETURN_T, None]:
        """return the current selected option as a tuple: (option, index)
        or as a list of tuples (in case multiselect==True)
        """
        if self.multiselect:
            return_tuples = []
            for selected in self.selected_indexes:
                return_tuples.append((self.options[selected], selected))
            return return_tuples
        else:
            filtered = self.get_filtered_options()
            if not filtered:
                return None
            if self.index >= len(filtered):
                self.index = 0
            orig_index, option = filtered[self.index]
            return option, orig_index

    def get_title_lines(self, *, max_width: int = 80) -> List[str]:
        lines = []
        if self.title:
            if "\n" in self.title:
                lines.extend(self.title.split("\n"))
            else:
                lines.extend(textwrap.fill(self.title, max_width - 2, drop_whitespace=False).split("\n"))
            lines.append("")
        
        if self.enable_search:
            lines.append(f"Search: {self._search_string}")
            lines.append("")

        return lines

    def get_option_lines(self) -> List[str]:
        lines: List[str] = []
        filtered = self.get_filtered_options()
        if not filtered:
            return ["No results"]
        
        for index, (orig_index, option) in enumerate(filtered):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * " "

            if self.multiselect:
                symbol = (
                    SYMBOL_CIRCLE_FILLED
                    if orig_index in self.selected_indexes
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

    def draw(self, screen: Backend) -> None:
        """draw the UI on the screen, handle scroll if needed"""
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
            if description_present and i >= title_length:
                screen.addnstr(y, x, line, max_x // 2 - 2)
            else:
                screen.addnstr(y, x, line, max_x - 2)
            y += 1

        filtered = self.get_filtered_options()
        if filtered and self.index < len(filtered):
            _, option = filtered[self.index]
            if isinstance(option, Option) and option.description is not None:
                description_lines = textwrap.fill(option.description, max_x // 2 - 2).split('\n')

                for i, line in enumerate(description_lines):
                    screen.addnstr(i + title_length, max_x // 2, line, max_x - 2)

        screen.refresh()

    def run_loop(
        self, screen: Backend, position: Position
    ) -> Union[List[PICK_RETURN_T], PICK_RETURN_T, None]:
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
            elif self.enable_search:
                if c in KEYS_BACKSPACE:
                    self._search_string = self._search_string[:-1]
                    self.index = 0
                    self._ensure_valid_selection()
                elif 0 <= c <= 255 and chr(c).isprintable():
                    self._search_string += chr(c)
                    self.index = 0
                    self._ensure_valid_selection()

    def _resolve_backend(self) -> Backend:
        if isinstance(self.backend, Backend):
            return self.backend
        if self.backend == "curses":
            return CursesBackend(screen=self.screen)
        if self.backend == "blessed":
            return BlessedBackend()
        raise ValueError(
            f"Unknown backend: {self.backend!r}. "
            "Use 'curses', 'blessed', or a Backend instance."
        )

    def config_curses(self) -> None:
        try:
            curses.use_default_colors()
            curses.curs_set(0)
        except Exception:
            curses.initscr()

    def _start(self, screen: "curses._CursesWindow"):
        self.config_curses()
        return self.run_loop(CursesBackend(screen=screen), self.position)

    def start(self):
        backend = self._resolve_backend()
        if isinstance(backend, CursesBackend) and backend._screen is not None:
            last_cur = curses.curs_set(0)
            ret = self.run_loop(backend, self.position)
            if last_cur:
                curses.curs_set(last_cur)
            return ret
        elif isinstance(backend, CursesBackend):
            def _curses_main(screen: "curses._CursesWindow"):
                backend._screen = screen
                backend.setup()
                return self.run_loop(backend, self.position)
            return curses.wrapper(_curses_main)
        else:
            backend.setup()
            try:
                return self.run_loop(backend, self.position)
            finally:
                backend.teardown()


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
    backend: Union[str, Backend] = "curses",
    enable_search: bool = False,
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
        backend,
        enable_search,
    )
    return picker.start()
