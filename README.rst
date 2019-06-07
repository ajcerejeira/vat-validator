=============
vat-validator
=============

Pythonic VAT validation library 🌍💳✔

.. image:: https://travis-ci.com/ajcerejeira/vat-validator.svg?branch=master
    :target: https://travis-ci.com/ajcerejeira/vat-validator

.. image:: https://readthedocs.org/projects/vat-validator/badge/?version=latest
    :target: https://vat-validator.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/ajcerejeira/vat-validator/badge.svg?branch=master
    :target: https://coveralls.io/github/ajcerejeira/vat-validator?branch=master

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black


Features
--------

- Offline VAT code validation using country specific regular expressions and
  checksum algorithms;
- Online validation for European Union VAT codes using VIES_ webservice;
- Fully annotated with type hints, for a better IDE and ``mypy`` development
  experience;
- Tested and validated against 1697 different VAT codes.

.. _VIES: http://ec.europa.eu/taxation_customs/vies/


===============
Getting started
===============

.. getting-started

Instalation
-----------

``vat-validator`` is distributed as standard pip library, and can be installed
by running:

::

    pip install vat-validator

To install the latest development version directly from git:

::

    pip install git+git://github.com/ajcerejeira/vat-validator.git


Usage
-----

>>> from vat_validator import validate_vat, countries_where_vat_is_valid
>>> validate_vat('PT', 'PT-980 405 319')
True


Contributing
============

Comming soon...


License
=======

This software is distrubuted under MIT license. See the LICENSE_ file for
details.

.. _LICENSE: LICENSE
