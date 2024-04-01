from pick import Picker, Option


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
    lines, current_line = picker.get_lines()
    assert current_line == 1


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
               Option("option3", description="description3"), Option("option4"), "option5"]
    picker = Picker(options)
    option, index = picker.get_selected()
    assert index == 0
    assert isinstance(option, Option)
    assert option.label == "option1"
    assert option.value == 101
    assert option.description == "description1"
    picker.move_down()
    option, index = picker.get_selected()
    assert index == 1
    assert isinstance(option, Option)
    assert option.label == "option2"
    assert option.value == 102
    picker.move_down()
    option, index = picker.get_selected()
    assert index == 2
    assert isinstance(option, Option)
    assert option.label == "option3"
    assert option.description == "description3"
    picker.move_down()
    option, index = picker.get_selected()
    assert index == 3
    assert isinstance(option, Option)
    assert option.label == "option4"
    picker.move_down()
    option, index = picker.get_selected()
    assert index == 4
    assert isinstance(option, str)


def test_parse_options():
    options = {"option1": "description1", "option2": ""}
    picker = Picker(options)
    option, index = picker.get_selected()
    assert index == 0
    assert isinstance(option, Option)
    assert option.description == "description1"
    picker.move_down()
    option, index = picker.get_selected()
    assert index == 1
    assert isinstance(option, Option)
    assert option.description is None
