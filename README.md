pick [![Build Status](https://travis-ci.org/wong2/pick.svg?branch=master)](https://travis-ci.org/wong2/pick)
====

**pick** is a small python library to help you create curses based interactive selection
list in the terminal. See it in action:

![Basic Demo](example/basic.gif?raw=true)
![Multiselect Demo](example/multiselect.gif?raw=true)


### Installation

    $ pip install pick

### Usage

**pick** comes with a simple api:

    >>> from pick import pick

    >>> title = 'Please choose your favorite programming language: '
    >>> options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
    >>> chosen_options = pick(options, title)
    >>> print chosen_options
    >>> [('Java', 0), ('PHP', 3), ('Haskell', 6)]

#### Options

* `options`: a list of options to choose from
* `title`: (optional) a title above options list
* `indicator`: (optional) custom the selection indicator, defaults to *
* `default_index`: (optional) set this if the default selected option is not the first one
* `chosen_indicator`: (optional) curses attribute to use when item has been chosen

#### Register custom handlers

sometimes you may need to register custom handlers to specific keys, you can use the `register_custom_handler` API:

    >>> from pick import Picker
    >>> title, options = 'Title', ['Option1', 'Option2']
    >>> picker = Picker(options, title)
    >>> def go_back(picker):
    ...     return None, -1
    >>> picker.register_custom_handler(ord('h'),  go_back)
    >>> options = picker.start()

* the custom handler will be called with the `picker` instance as it's parameter.
* the custom handler should either return a list of a two element tuple, or None.
* if None is returned, the picker would continue to run, otherwise the picker will stop and return the list of tuples.

