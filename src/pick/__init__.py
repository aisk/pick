#!/usr/bin/env python

from collections import namedtuple
from dataclasses import dataclass, field
from typing import (
    Any,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)
import blessed

__all__ = ["pick", "Picker", "Option"]

SYMBOL_CIRCLE_FILLED = "(x)"
SYMBOL_CIRCLE_EMPTY = "( )"


@dataclass
class Option:
    label: str
    value: Any = None
    description: Optional[str] = None
    enabled: bool = True

    def __str__(self) -> str:
        return (
            f"{self.label}{' (' + self.description + ')' if self.description else ''}"
        )


OPTION_T = Union[Option, str]
PICK_RETURN_T = Tuple[OPTION_T, int]

Position = namedtuple("Position", ["y", "x"])


def _display_screen(
    term: blessed.Terminal,
    indicator: str,
    title: Optional[str],
    choices: Sequence[OPTION_T],
    index: int,
    selected_indexes: list[int],
    multiselect: bool,
) -> None:
    if title:
        print(title)

    for idx, val in enumerate(choices):
        selectable = ""
        if isinstance(val, Option) and not val.enabled:
            selectable = term.gray35

        is_selected = ""
        if multiselect:
            is_selected = (
                f"{SYMBOL_CIRCLE_EMPTY} "
                if idx not in selected_indexes
                else f"{SYMBOL_CIRCLE_FILLED} "
            )

        if idx == index:
            print(f"{indicator} {selectable}{is_selected}{val}{term.normal}")
        else:
            print(
                f"{' ' * (len(indicator) + 1)}{selectable}{is_selected}{val}{term.normal}"
            )


@dataclass
class Picker:
    options: Sequence[OPTION_T]
    title: Optional[str] = None
    indicator: str = "*"
    default_index: int = 0
    multiselect: bool = False
    min_selection_count: int = 0
    selected_indexes: List[int] = field(init=True, default_factory=list)
    index: int = field(init=True, default=0)
    position: Position = Position(0, 0)
    clear_screen: bool = True
    quit_keys: Optional[Iterable[int]] = None
    term: blessed.Terminal = None
    # ) -> List[PICK_RETURN_T]:

    # screen: Optional["curses._CursesWindow"] = None
    def __post_init__(self) -> None:
        if len(self.options) == 0:
            raise ValueError("options should not be an empty list")

        if self.default_index >= len(self.options):
            raise ValueError("default_index should be less than the length of options")

        if self.multiselect and self.min_selection_count > len(self.options):
            raise ValueError(
                "min_selection_count is bigger than the available options, you will not be able to make any selection"
            )

        if all(
            isinstance(option, Option) and not option.enabled for option in self.options
        ):
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
            item = self.options[self.index]
            if (isinstance(item, Option) and item.enabled) or not isinstance(
                item, Option
            ):
                if self.index in self.selected_indexes:
                    self.selected_indexes.remove(self.index)
                else:
                    self.selected_indexes.append(self.index)

    def get_selected(self) -> Union[List[PICK_RETURN_T], PICK_RETURN_T]:
        """Return the current selected option as a tuple: (option, index)
        or as a list of tuples (in case multiselect==True)
        """
        if self.multiselect:
            return (
                [(self.options[idx], idx) for idx in self.selected_indexes]
                if self.multiselect
                else (self.options[self.index], self.index)
            )
        else:
            return self.options[self.index], self.index

    def start(self):
        _quit_keys: list[str] = (
            []
            if self.quit_keys is None
            else [chr(key_code) for key_code in self.quit_keys]
        )
        errmsg = ""

        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            print(self.term.clear())
            _display_screen(
                self.term,
                self.indicator,
                self.title,
                self.options,
                self.index,
                self.selected_indexes,
                self.multiselect,
            )

            selection_inprogress = True
            while selection_inprogress:
                key = self.term.inkey()
                if key.is_sequence or key == " ":
                    if key.name in {"KEY_TAB", "KEY_DOWN"}:
                        self.move_down()
                    elif key.name == "KEY_UP":
                        self.move_up()
                    elif key == " " and self.multiselect:
                        self.mark_index()
                    elif key.name == "KEY_ENTER":
                        if (
                            self.multiselect
                            and len(self.selected_indexes) < self.min_selection_count
                        ):
                            errmsg = f"{self.term.red}Must select at least {self.min_selection_count} entry(s)!{self.term.normal}"
                        else:
                            return self.get_selected()
                else:
                    if key.lower() in _quit_keys:
                        return None, -1

                self.index = self.index % len(self.options)

                print(self.term.clear())

                if errmsg:
                    print(errmsg)
                    errmsg = ""

                _display_screen(
                    self.term,
                    self.indicator,
                    self.title,
                    self.options,
                    self.index,
                    self.selected_indexes,
                    self.multiselect,
                )

        return self.get_selected()


def pick(
    options: Sequence[OPTION_T],
    title: Optional[str] = None,
    indicator: str = "*",
    default_index: int = 0,
    multiselect: bool = False,
    min_selection_count: int = 0,
    position: Position = Position(0, 0),
    clear_screen: bool = True,
    quit_keys: Optional[Iterable[int]] = None,
) -> Union[List[PICK_RETURN_T], Optional[PICK_RETURN_T]]:
    term = blessed.Terminal()
    picked = None

    with term.fullscreen(), term.cbreak():
        print(Picker(["a"], "a"))
        print("???")
        picked = Picker(
            options=options,
            title=title,
            indicator=indicator,
            default_index=default_index,
            multiselect=multiselect,
            min_selection_count=min_selection_count,
            selected_indexes=[],
            index=0,
            clear_screen=clear_screen,
            position=position,
            quit_keys=quit_keys,
            term=term,
        ).start()

    return picked if multiselect else (picked[0] if picked else None)


print(
    "Picked: ",
    pick(
        [
            Option(
                "Option 1",
                "option 1",
                "this is option 1 and is not selectable",
                enabled=False,
            ),
            "option 2",
            "option 3",
            Option(
                "Option 4",
                "option 4",
                "this is option 4 and selectable",
                enabled=True,
            ),
        ],
        "(Up/down/tab to move; space to select/de-select; Enter to continue)",
        indicator="=>",
        multiselect=True,
        quit_keys=[ord("q")],
        clear_screen=False,
        min_selection_count=2,
    ),
)
print()

print(
    "Picked: ",
    pick(
        ["Choice1", "choice 2", "choice3"],
        "(Up/down/tab to move; Enter to select)",
        indicator="=>",
        multiselect=False,
        quit_keys=[ord("q")],
    ),
)
