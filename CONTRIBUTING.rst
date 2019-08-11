============
Contributing
============

.. begin-contributing

Setting up
==========

It is recommended to set up a virtual environment to develop on this project.
To create one and install the required dependencies, run:

::

    python -m venv venv
    pip install -r requirements.txt

And you can start coding right ahead 🎉🎉🎉!


Documentation
=============

The documentation is built with Sphinx documentation generator.
To install Sphinx and the required plugins used in this project, run:

.. code:: bash

    pip install -r docs/requirements.txt


To build the documentation:

.. code:: bash

    cd docs/
    make html   # or .\make.bat html if you are on a Windows platform


Testing
=======

Currently the tests are implemented with standard Python unit testing framework
``unittest``, and are stored in ``tests/`` directory.

To run the tests:

::

    python -m unittest


Code style and linting
======================

This project uses mypy_, flake8_ and black_ code style and formatter.
This commands must return valid values on each commit:

::

    mypy -m vat_validator
    flake8 vat_validator tests
    black -l 79 --check vat_validator/ tests/

.. _mypy: http://www.mypy-lang.org/
.. _flake8: http://flake8.pycqa.org/
.. _black: https://github.com/python/black


It is recommended to set up your text editor/IDE to run this tools on save.
