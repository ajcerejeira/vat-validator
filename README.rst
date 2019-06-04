=============
vat-validator
=============

Pythonic VAT validation library

.. image:: https://travis-ci.com/ajcerejeira/vat-validator.svg?branch=master
    :target: https://travis-ci.com/ajcerejeira/vat-validator

.. image:: https://readthedocs.org/projects/vat-validator/badge/?version=latest
    :target: https://vat-validator.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/ajcerejeira/vat-validator/badge.svg?branch=master
    :target: https://coveralls.io/github/ajcerejeira/vat-validator?branch=master


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

>>> from vat_validator import validate_vat
>>> validate_vat('PT', 'PT-980 405 319')
True