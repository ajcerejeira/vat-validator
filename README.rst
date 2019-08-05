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

.. image:: https://img.shields.io/github/license/ajcerejeira/vat-validator
    :target: https://github.com/ajcerejeira/vat-validator/blob/master/LICENSE.txt
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

Installation
============

``vat-validator`` is distributed as standard pip library, and can be installed
by running:

::

    pip install vat-validator

To install the latest development version directly from git:

::

    pip install git+git://github.com/ajcerejeira/vat-validator.git


Usage
=====

>>> from vat_validator import inspect_vat, sanitize_vat, vat_is_valid
>>> vat_is_valid('PT', 'PT 502 011 378')
True
>>> sanitize_vat('PT', 'PT 502 011 378')
'502011378'


To validate a VAT number with ``VIES`` webservice:

>>> from vat_validator.vies import check_vat
>>> check_vat('PT', '502 011 378')
CheckVATResult(country_code='PT', vat='502011378', request_date=datetime.date(2019, 6, 8), valid=True, name='UNIVERSIDADE DO MINHO', address='LG DO PACO\nBRAGA\n4700-320 BRAGA')

.. end-getting-started


=======
Roadmap
=======

These are the goals before the `1.0.0` release:

- ❌ Have a comprehensive test suite with valid and invalid VAT codes
  for each country.
- ❌ Compare the validity of each VAT code used in tests with ``TIN``
  webservice.
- ✅ Remove ``zeep`` dependency, by using standard library ``urllib`` to make
  SOAP requests to VIES webservice, making this a module without any
  dependencies.
- ❌ Add support for ``async`` requests to VIES webservice.


============
Contributing
============

Pull requests are welcome! Please check the :doc:`CONTRIBUTING <contributing>`
file for contribution guidelines.

=======
License
=======

This software is distributed under MIT license. See the :doc:`LICENSE <license>`
file for details.

