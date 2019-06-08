=============
vat-validator
=============

Pythonic VAT validation library 🌍💳✅

.. image:: https://travis-ci.com/ajcerejeira/vat-validator.svg?branch=master
    :target: https://travis-ci.com/ajcerejeira/vat-validator
    :alt: Build status

.. image:: https://readthedocs.org/projects/vat-validator/badge/?version=latest
    :target: https://vat-validator.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/ajcerejeira/vat-validator/badge.svg?branch=master
    :target: https://coveralls.io/github/ajcerejeira/vat-validator?branch=master
    :alt: Coverage status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: Code style: black

.. image:: https://img.shields.io/github/license/ajcerejeira/vat-validator.svg
    :target: https://github.com/ajcerejeira/vat-validator/blob/master/LICENSE
    :alt: License: MIT

.. image:: https://img.shields.io/pypi/v/vat-validator.svg
    :target: https://pypi.org/project/vat-validator/
    :alt: PyPI

Features
========

- Offline VAT code validation using country specific regular expressions and
  checksum algorithms;
- Online validation for European Union VAT codes using VIES_ webservice;
- VAT code sanitization;
- Fully annotated with type hints, for a better IDE and ``mypy`` development
  experience;
- Tested and validated against 1697 different VAT codes.

.. _VIES: http://ec.europa.eu/taxation_customs/vies/


===============
Getting started
===============

.. begin-getting-started

Instalation
===========

``vat-validator`` is distributed as standard pip library, and can be installed
by running:

::

    pip install vat-validator

To install the latest development version directly from git:

::

    pip install git+git://github.com/ajcerejeira/vat-validator.git


Usage
=====

>>> from vat_validator import validate_vat, countries_where_vat_is_valid
>>> validate_vat('PT', 'PT 502 011 378')
True
>>> countries_where_vat_is_valid('502 011 378')
['PT']

>>> from vat_validator.vies import check_vat
>>> check_vat('PT', '502 011 378')
CheckVATResult(country_code='PT', vat='502011378', request_date=datetime.date(2019, 6, 8), valid=True, name='UNIVERSIDADE DO MINHO', address='LG DO PACO\nBRAGA\n4700-320 BRAGA')

.. end-getting-started


============
Contributing
============

Pull requests are welcome! Please check the CONTRIBUTING_ file for contribution guidelines.

.. _CONTRIBUTING: CONTRIBUTING.rst


=======
License
=======

This software is distrubuted under MIT license. See the LICENSE_ file for details.

.. _LICENSE: LICENSE
