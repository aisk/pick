#!/usr/bin/env python

from collections import namedtuple
from dataclasses import dataclass, field
from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
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
_pick_type = Tuple[Optional[OPTION_T], int]
PICK_RETURN_T = Union[List[_pick_type], _pick_type]

Position = namedtuple("Position", ["y", "x"])


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
    term: Optional[blessed.Terminal] = None
    idxes_in_scope: List[int] = field(init=False, default_factory=list)
    filter: str = field(init=False, default_factory=str)

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
        if self.term is None:
            self.term = blessed.Terminal()

        if all(
            isinstance(option, Option) and not option.enabled for option in self.options
        ):
            raise ValueError(
                "all given options are disabled, you must at least have one enabled option."
            )

        self.index = self.default_index
        option = self.options[self.index]
        self.idxes_in_scope = list(range(len(self.options)))
        self.filter = ""
        if isinstance(option, Option) and not option.enabled:
            self.move_down()

    def move_up(self) -> None:
        if not self.idxes_in_scope:
            # user pressed up/down with a filter with no items;
            # break out or else it will infinitely decrement index
            return

        while True:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.options) - 1
            option = self.options[self.index]
            if self.index not in self.idxes_in_scope:
                continue
            if not isinstance(option, Option) or option.enabled:
                break

    def move_down(self) -> None:
        if not self.idxes_in_scope:
            # user pressed up/down with a filter with no items;
            # break out or else it will infinitely decrement index
            return

        while True:
            self.index += 1
            if self.index >= len(self.options):
                self.index = 0
            option = self.options[self.index]

            if self.index not in self.idxes_in_scope:
                continue

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

    def get_title_lines(self) -> List[str]:
        if self.title:
            return [self.title, ""]
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

    def get_lines(self) -> Tuple[List[str], int]:
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def get_selected(self) -> PICK_RETURN_T:
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

    def start(self) -> PICK_RETURN_T:
        self.term = cast(blessed.Terminal, self.term)
        _quit_keys: list[str] = (
            []
            if self.quit_keys is None
            else [chr(key_code) for key_code in self.quit_keys]
        )
        errmsg = ""

        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            print(self.term.clear())
            self._display_screen()

            selection_inprogress = True
            while selection_inprogress:
                key = self.term.inkey()
                if key.is_sequence or key == " ":
                    if key.name in {"KEY_TAB", "KEY_DOWN"}:
                        self.move_down()
                    elif key.name == "KEY_UP":
                        self.move_up()
                    elif (
                        key == " "
                        and self.multiselect
                        and len(self.idxes_in_scope) != 0
                    ):
                        self.mark_index()
                    elif key.name == "KEY_ENTER":
                        if (
                            self.multiselect
                            and len(self.selected_indexes) < self.min_selection_count
                        ):
                            errmsg = f"{self.term.red}Must select at least {self.min_selection_count} entry(s)!{self.term.normal}"
                        else:
                            return self.get_selected()
                    elif key.name == "KEY_BACKSPACE":
                        self.filter = self.filter[:-1] if self.filter else ""
                else:
                    if key.lower() in _quit_keys:
                        return None, -1
                    else:
                        # Keystroke gets appended to the current filter
                        self.filter += key

                print(self.term.clear())

                if errmsg:
                    print(errmsg)
                    errmsg = ""

                if self.filter:
                    print(
                        f"Currently filtering by: {self.term.yellow}'{self.filter}...'{self.term.normal}"
                    )

                self._display_screen()

        return self.get_selected()

    def _display_screen(self) -> None:
        self.term = cast(blessed.Terminal, self.term)
        # options_with_idx is used instead of just self.options because
        # we need to be able to keep track of the original item's index
        # in the case that we're filtering
        options_with_idx = [c for c in enumerate(self.options)]

        if self.filter:
            options_with_idx = [
                choice
                for choice in options_with_idx
                if str(choice[1]).startswith(self.filter)
            ]

        if not options_with_idx:
            self.idxes_in_scope = []
            print(
                f"{self.term.red}No matching results, please press backspace to unfilter...{self.term.normal}"
            )
            return

        # Chunk logic stuff is required to do scrolling when too many
        # vertical items
        chunk_by = self.term.height - 7

        chunked_choices = [
            options_with_idx[i : i + chunk_by]
            for i in range(0, len(options_with_idx), chunk_by)
        ]

        chunk_to_render = 0
        for i, chunk in enumerate(chunked_choices):
            if self.index in [p[0] for p in chunk]:
                chunk_to_render = i

        # need to set this so that when we're doing a command thats not
        # modifying the filter (i.e up/down) we need to be able to tell
        # whether the cursor is in scope
        self.idxes_in_scope = [pair[0] for chunk in chunked_choices for pair in chunk]

        # can't do this bc the index's aren't guarunteed to be consecutive
        # outside the first iteration:
        #   chunk_to_render = self.index // chunk_by

        if self.title:
            print(self.title)

        if chunk_to_render > 0:
            print("  ( scroll up to reveal previous entries )")

        for val in chunked_choices[chunk_to_render]:
            selectable = ""
            if isinstance(val[1], Option) and not val[1].enabled:
                selectable = self.term.gray35

            is_selected = ""
            if self.multiselect:
                is_selected = (
                    f"{SYMBOL_CIRCLE_EMPTY} "
                    if val[0] not in self.selected_indexes
                    else f"{SYMBOL_CIRCLE_FILLED} "
                )

            if val[0] == self.index:
                print(
                    f"{self.indicator} {selectable}{is_selected}{val[1]}{self.term.normal}"
                )
            else:
                print(
                    f"{' ' * (len(self.indicator) + 1)}{selectable}{is_selected}{val[1]}{self.term.normal}"
                )

        if chunk_to_render < len(chunked_choices) - 1:
            print(f"  ( scroll down to reveal additional entries )")


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
) -> PICK_RETURN_T:
    term = blessed.Terminal()
    picked = None
    with (
        term.fullscreen(),
        term.cbreak(),
        term.location(position.x, position.y),
    ):
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

    return picked


if __name__ == "__main__":
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
