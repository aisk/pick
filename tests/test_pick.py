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
    _, current_line = picker.get_lines()
    assert current_line == 1


def test_pick_list_of_non_str_and_option():
    # More details: https://github.com/aisk/pick/issues/120
    options = [{"key1": "value1"}, {"key2", "value2"}]
    picker = Picker(options)
    lines, _ = picker.get_lines()
    assert lines == ["* {'key1': 'value1'}", "  {'key2', 'value2'}"]


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
        assert isinstance(option[0], Option)
    option = selected_options[0]
    assert option[0].label == "option1"
    assert option[0].value == 101
    assert option[0].description == "description1"
