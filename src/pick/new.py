#!/usr/bin/env python

from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Container, Iterable, Optional, Sequence, Tuple, TypeVar, Union
import blessed

__all__ = ["pick", "Option"]

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


OPTION_T = TypeVar("OPTION_T", str, Option)
PICK_RETURN_T = Tuple[OPTION_T, int]

Position = namedtuple("Position", ["y", "x"])


def _display_screen(
    term: blessed.Terminal,
    indicator: str,
    title: Optional[str],
    choices: Sequence[OPTION_T],
    selection_idx: int,
    selected: list[int],
    multiselect: bool,
):
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
                if idx not in selected
                else f"{SYMBOL_CIRCLE_FILLED} "
            )

        if idx == selection_idx:
            print(f"{indicator} {selectable}{is_selected}{val}{term.normal}")
        else:
            print(
                f"{' ' * (len(indicator) + 1)}{selectable}{is_selected}{val}{term.normal}"
            )


def _select(
    options: Sequence[OPTION_T],
    term: blessed.Terminal,
    indicator: str,
    title: Optional[str],
    choices: Sequence[OPTION_T],
    selection_idx: int,
    selected: set[int],
    multiselect: bool,
    quit_keys: Optional[Union[Container[int], Iterable[int]]] = None,
    min_selection_count: int = 0,
):
    if not quit_keys:
        quit_keys = []
    else:
        quit_keys = [chr(key_code) for key_code in quit_keys]
    errmsg = ""
    with term.fullscreen(), term.cbreak():
        print(term.clear())
        _display_screen(
            term, indicator, title, options, selection_idx, selected, multiselect
        )

        selection_inprogress = True
        while selection_inprogress:
            key = term.inkey()
            if key.is_sequence or key == " ":
                if key.name in {"KEY_TAB", "KEY_DOWN"}:
                    selection_idx += 1
                elif key.name == "KEY_UP":
                    selection_idx -= 1
                elif key == " " and multiselect:
                    item = options[selection_idx]
                    if (isinstance(item, Option) and item.enabled) or not isinstance(
                        item, Option
                    ):
                        if selection_idx not in selected:
                            selected.add(selection_idx)
                        else:
                            selected.remove(selection_idx)
                elif key.name == "KEY_ENTER":
                    if multiselect:
                        if len(selected) < min_selection_count:
                            errmsg = f"{term.red}Must select at least {min_selection_count} entry(s)!{term.normal}"
                        else:
                            selection_inprogress = False
                    else:
                        selected.add(selection_idx)
                        selection_inprogress = False
            else:
                if key.lower() in quit_keys:
                    selection_inprogress = False

            selection_idx = selection_idx % len(options)

            print(term.clear())

            if errmsg:
                print(errmsg)
                errmsg = ""

            _display_screen(
                term, indicator, title, options, selection_idx, selected, multiselect
            )

    return [options[idx] for idx in selected]


def pick(
    options: Sequence[OPTION_T],
    title: Optional[str] = None,
    indicator: str = "*",
    default_index: int = 0,
    multiselect: bool = False,
    min_selection_count: int = 0,
    position: Position = Position(0, 0),
    clear_screen: bool = True,
    quit_keys: Optional[Union[Container[int], Iterable[int]]] = None,
):
    term = blessed.Terminal()
    picked = None

    with term.fullscreen(), term.cbreak():
        picked = _select(
            options,
            term,
            indicator,
            title,
            options,
            0,
            set(),
            multiselect,
            quit_keys,
            min_selection_count,
        )

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
