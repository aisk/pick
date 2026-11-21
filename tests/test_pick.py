from typing import Tuple

import pytest

from pick import Backend, Option, Picker


def test_move_up_down():
    title = "Please choose an option: "
    options = ["option1", "option2", "option3"]
    picker = Picker(options, title)
    picker.move_up()
    assert picker.get_selected() == ("option3", 2)
    picker.move_down()
    picker.move_down()
    assert picker.get_selected() == ("option2", 1)


def test_default_index():
    title = "Please choose an option: "
    options = ["option1", "option2", "option3"]
    picker = Picker(options, title, default_index=1)
    assert picker.get_selected() == ("option2", 1)


def test_get_lines():
    title = "Please choose an option: "
    options = ["option1", "option2", "option3"]
    picker = Picker(options, title, indicator="*")
    lines, current_line = picker.get_lines()
    assert lines == [title, "", "* option1", "  option2", "  option3"]
    assert current_line == 3


def test_no_title():
    options = ["option1", "option2", "option3"]
    picker = Picker(options)
    _, current_line = picker.get_lines()
    assert current_line == 1


def test_pick_list_of_non_str_and_option():
    # More details: https://github.com/aisk/pick/issues/120
    options = [{"key1": "value1"}, {"key2": "value2"}]
    picker = Picker(options)  # type: ignore
    lines, _ = picker.get_lines()
    assert lines == ["* {'key1': 'value1'}", "  {'key2': 'value2'}"]


def test_multi_select():
    title = "Please choose an option: "
    options = ["option1", "option2", "option3"]
    picker = Picker(options, title, multiselect=True, min_selection_count=1)
    assert picker.get_selected() == []
    picker.mark_index()
    assert picker.get_selected() == [("option1", 0)]
    picker.move_down()
    picker.mark_index()
    assert picker.get_selected() == [("option1", 0), ("option2", 1)]


def test_option():
    options = [Option("option1", 101, "description1"), Option("option2", 102),
               Option("option3", description="description3"), Option("option4")]
    picker = Picker(options, multiselect=True)
    for _ in range(4):
        picker.mark_index()
        picker.move_down()
    selected_options = picker.get_selected()
    for option in selected_options:
        assert isinstance(option, tuple)
        assert isinstance(option[0], Option)
    option = selected_options[0]
    assert option[0].label == "option1"
    assert option[0].value == 101
    assert option[0].description == "description1"

def test_disabled_option():
    options = [Option("option1"), Option("option2", enabled=False), Option("option3")]
    picker = Picker(options)
    assert picker.get_selected() == (Option("option1"), 0)
    picker.move_down()
    assert picker.get_selected() == (Option("option3"), 2)

def test_negative_default_index():
    options = ["option1", "option2", "option3"]
    picker = Picker(options, default_index=-1)
    assert picker.get_selected() == ("option3", 2)
    lines, _ = picker.get_lines()
    assert "* option3" in lines

    picker = Picker(options, default_index=-3)
    assert picker.get_selected() == ("option1", 0)

    with pytest.raises(ValueError):
        Picker(options, default_index=-4)
    with pytest.raises(ValueError):
        Picker(options, default_index=3)


def test_mark_index_disabled_option():
    options = [Option("option1"), Option("option2", enabled=False), Option("option3")]
    picker = Picker(options, multiselect=True)
    picker.index = 1  # Point directly to disabled option2
    picker.mark_index()
    assert picker.get_selected() == []  # Disabled option should NOT be marked


def test_select_all_and_deselect_all():
    options = [Option("option1"), Option("option2", enabled=False), Option("option3")]
    picker = Picker(options, multiselect=True)
    picker.select_all()
    # Should only select option1 (0) and option3 (2), ignoring disabled option2 (1)
    assert picker.get_selected() == [(Option("option1"), 0), (Option("option3"), 2)]
    picker.deselect_all()
    assert picker.get_selected() == []


class FakeScreen(Backend):
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.clear()

    def setup(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def clear(self) -> None:
        self.grid = [[" "] * self.width for _ in range(self.height)]

    def getmaxyx(self) -> Tuple[int, int]:
        return self.height, self.width

    def addnstr(self, y: int, x: int, s: str, n: int) -> None:
        for i, ch in enumerate(s[:n]):
            self.grid[y][x + i] = ch

    def getch(self) -> int:
        return -1

    def refresh(self) -> None:
        pass

    def row(self, y: int) -> str:
        return "".join(self.grid[y]).rstrip()


def test_draw_truncates_first_option_when_description_present():
    options = [
        Option("first option has a really really long label", description="short"),
        Option("second", description="desc 2"),
    ]
    picker = Picker(options, title="title")
    screen = FakeScreen(height=10, width=60)
    picker.draw(screen)
    # row 0: title, row 1: blank, row 2: first option + its description
    # option label is truncated to max_x // 2 - 2 = 28 chars, description starts at max_x // 2 = 30
    assert screen.row(2) == "* first option has a really ".ljust(30) + "short"
