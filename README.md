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

- `options`: a list of options to choose from
- `title`: (optional) a title above options list
- `indicator`: (optional) custom the selection indicator, defaults to `*`
- `default_index`: (optional) set this if the default selected option
  is not the first one
- `multiselect`: (optional), if set to True its possible to select
  multiple items by hitting SPACE
- `min_selection_count`: (optional) for multi select feature to
  dictate a minimum of selected items before continuing
- `screen`: (optional), if you are using `pick` within an existing curses application set this to your existing `screen` object. It is assumed this has initialised in the standard way (e.g. via `curses.wrapper()`, or `curses.noecho(); curses.cbreak(); screen.kepad(True)`)
- `position`: (optional), if you are using `pick` within an existing curses application use this to set the first position to write to. e.g., `position=pick.Position(y=1, x=1)`
- `quit_keys`: (optional), if you want to quit early, you can pass a key codes.
  If the corresponding key are pressed, it will quit the menu.

## Community Projects

[pickpack](https://github.com/anafvana/pickpack): A fork of `pick` to select tree data.
