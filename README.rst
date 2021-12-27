pick
====

.. image:: https://github.com/wong2/pick/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/wong2/pick/actions/workflows/ci.yml

.. image:: https://img.shields.io/pypi/v/pick.svg
   :alt: PyPI
   :target: https://pypi.python.org/pypi/pick
   
.. image:: https://img.shields.io/pypi/dm/pick
   :alt: PyPI
   :target: https://pypi.python.org/pypi/pick
   
|

**pick** is a small python library to help you create cursor-based interactive selection list in the terminal. 

.. image:: https://github.com/wong2/pick/raw/master/example/basic.gif
   :alt: Demo

Installation
------------

::

    $ pip install pick

Usage
-----

**pick** comes with a simple api::

    >>> from pick import pick

    >>> title = 'Please choose your favorite programming language: '
    >>> options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
    >>> option, index = pick(options, title)
    >>> print(option)
    >>> print(index)

**outputs**::

    >>> C++
    >>> 4

**pick** multiselect example::

    >>> from pick import pick

    >>> title = 'Please choose your favorite programming language (press SPACE to mark, ENTER to continue): '
    >>> options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
    >>> selected = pick(options, title, multiselect=True, min_selection_count=1)
    >>> print(selected)

**outputs**::

    >>> [('Java', 0), ('C++', 4)]


Options
-------

* ``options``: a list of options to choose from
* ``title``: (optional) a title above options list
* ``indicator``: (optional) custom the selection indicator, defaults to *
* ``default_index``: (optional) set this if the default selected option is not the first one
* ``multiselect``: (optional), if set to True its possible to select multiple items by hitting SPACE
* ``min_selection_count``: (optional) for multi select feature to dictate a minimum of selected items before continuing
* ``options_map_func``: (optional) a mapping function to pass each option through before displaying

Register custom handlers
------------------------

Sometimes you may need to register custom handlers for specific keyboard keys, you can use the ``register_custom_handler`` API::

    >>> from pick import Picker
    >>> title, options = 'Title', ['Option1', 'Option2']
    >>> picker = Picker(options, title)
    >>> def go_back(picker):
    ...     return None, -1
    >>> picker.register_custom_handler(ord('h'),  go_back)
    >>> option, index = picker.start()

* the custom handler will be called with the ``picker`` instance as it's parameter.
* the custom handler should either return a two element tuple, or None.
* if None is returned, the picker would continue to run, otherwise the picker will stop and return the tuple.

Options Map Function
--------------------

If your options are not in a format that you want displayed (such as a dictionary), you can pass in a mapping function which each option will be run through. The return value of the function will be displayed.

* the selected option returned will be the original value and not the displayed return result from the ``options_map_func`` function.

**pick** options map function example::

    >>> from pick import pick

    >>> title = 'Please choose an option: '
    >>> options = [{'label': 'option1'}, {'label': 'option2'}, {'label': 'option3'}]

    >>> def get_label(option): return option.get('label')

    >>> selected = pick(options, title, indicator='*', options_map_func=get_label)
    >>> print(selected)

**displays**::

    Please choose an option:

    * option1
      option2
      option3

**outputs**::

    >>> ({ 'label': 'option1' }, 0)
