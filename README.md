pick
====

**pick** is a small python library to help you create curses based interactive selection
list in the terminal. See it in action:

![Demo](example/basic.gif?raw=true)


### Installation

    $ pip install pick

### Usage

**pick** comes with a simple api:

    >>> from pick import pick

    >>> title = 'Please choose your favorite programming language: '
    >>> options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
    >>> option, index = pick(options, title)

#### Options

* `options`: a list of options to choose from
* `title`: (optional) a title above options list
* `indicator`: (optional) custom the selection indicator
* `default_index`: (optional) set this if the default selected option is not the first one
