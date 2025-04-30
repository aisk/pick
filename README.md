# pick

[![image](https://github.com/aisk/pick/actions/workflows/ci.yml/badge.svg)](https://github.com/aisk/pick/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pick.svg)](https://pypi.python.org/pypi/pick)
[![PyPI](https://img.shields.io/pypi/dm/pick)](https://pypi.python.org/pypi/pick)

**pick** is a small python library to help you create curses based
interactive selection list in the terminal.

|         Basic          |         Multiselect          |
| :--------------------: | :--------------------------: |
| ![](example/basic.gif) | ![](example/multiselect.gif) |

## Installation

    $ pip install pick

## Usage

**pick** comes with a simple api:

    >>> from pick import pick

    >>> title = 'Please choose your favorite programming language: '
    >>> options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
    >>> option, index = pick(options, title)
    >>> print(option)
    >>> print(index)

**outputs**:

    >>> C++
    >>> 4

**pick** multiselect example:

    >>> from pick import pick

    >>> title = 'Please choose your favorite programming language (press SPACE to mark, ENTER to continue): '
    >>> options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
    >>> selected = pick(options, title, multiselect=True, min_selection_count=1)
    >>> print(selected)

**outputs**:

    >>> [('Java', 0), ('C++', 4)]

## Options

### `Option`

Provides a an alternative to a simple string value to select from.

- `label`: The string of the option that is displayed in the menu
- `value`: Optional different value to assign to the option to leverage
  once selected.
- `description`: Optional text that is rendered alongside the label in the
  menu.
- `enabled`: Whether the option is selectable. By default, is `True`.
- `color`: The color the option is printed with to the menu. By default
  is colorless. Accepts a string like ANSI code. e.g. to make it bold red:
  `color='\x1b[1;31m'`; can also use codes from blessed like
  `color=Terminal().green`)

Is leveraged by passing in to `pick()`:

```python
pick(
    options=[
        Option(
            "Option 1",
            "option_1_value",
            "This is option 1 and is not selectable",
            enabled=False,
        ),
        "option 2",
        "option 3",
        Option(
            "Option 4",
            "option 4",
            "This is option 4 and selectable and green",
            enabled=True,
            color=blessed.Terminal().green,
        ),
        "option 5",
        Option(
            "Option 6",
            "option 6",
            "this is option 6 and colored but unselectable",
            enabled=False,
            color=blessed.Terminal().pink,
        ),
        "option 5",
    ],
    ...
)
```

### `pick`

- `options`: a list of options to choose from
- `title`: (optional) a title above options list
- `indicator`: (optional) custom the selection indicator, defaults to `*`
- `default_index`: (optional) set this if the default selected option
  is not the first one
- `multiselect`: (optional), if set to True its possible to select
  multiple items by hitting SPACE
- `min_selection_count`: (optional) for multi select feature to
  dictate a minimum of selected items before continuing
- `position`: (optional), if you are using `pick` within an existing curses application use this to set the first position to write to. e.g., `position=pick.Position(y=1, x=1)`
- `quit_keys`: (optional), if you want to quit early, you can pass a key codes.
  If the corresponding key are pressed, it will quit the menu.
- `disabled_color`: (optional) if you want to change the color that disabled options are; by default, is grey. Accepts a string like ANSI code. e.g. to make them bold red: `disabled_color='\x1b[1;31m'`; can also use codes from blessed like `disabled_color=Terminal().yellow`; to make it not-colored, `disabled_color=""`)
- `pagination_color`: (optional) if you want to change the color that the pagination messages (shown when there is multiple pages of content to scroll through); by default, is uncolored. Accepts a string like ANSI code. e.g. to make them bold red: `pagination_color='\x1b[1;31m'`; can also use codes from blessed like `pagination=Terminal().yellow`)

## Community Projects

[pickpack](https://github.com/anafvana/pickpack): A fork of `pick` to select tree data.
